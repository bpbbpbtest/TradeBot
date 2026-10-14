"""Main orchestrator: wires data, strategy, engine, and reporting.

Run with:  python -m tradebot.main [--config config.yaml] [--duration SEC]

The bot connects to Bitpin public WebSocket channels, computes the four
order-book-imbalance features, and simulates a long-only strategy against
the live book. No real orders are ever placed.

Trading can be stopped/started and the symbol switched at runtime from the
local dashboard (http://127.0.0.1:8765) without restarting the process.
"""

from __future__ import annotations

import argparse
import asyncio
import gzip
import logging
import os
import shutil
import signal
import time
from pathlib import Path
from typing import Any

from tradebot.api.rest_client import BitpinRestClient, CommissionInfo
from tradebot.api.ws_client import BitpinWsClient
from tradebot.config import Config, load_config
from tradebot.dashboard import DashboardServer, DashboardState
from tradebot.data.orderbook import OrderBookState
from tradebot.data.recorder import RawDataRecorder
from tradebot.data.trades import TradesStream
from tradebot.engine.exits import ExitRules
from tradebot.engine.maker_engine import MakerEngine
from tradebot.engine.paper_engine import ExitReason, PaperEngine
from tradebot.engine.risk import RiskManager
from tradebot.report.metrics import ReportWriter
from tradebot.strategy.edge import EdgeEstimator
from tradebot.strategy.features import FeatureEngine
from tradebot.strategy.scoring import Scorer

logger = logging.getLogger("tradebot")

_SYMBOLS_CACHE_SEC = 120.0
_INSTANCE_LOCK: Any = None


class TradingBot:
    """Single-symbol paper-trading bot with runtime start/stop/symbol switch."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._rest = BitpinRestClient(config)
        self._recorder = RawDataRecorder(config.paths.raw_dir)
        self._exits = ExitRules(config.exit, config.risk)
        self._dashboard_state = DashboardState(
            max_history=config.dashboard.history_max_points
        )
        self._dashboard: DashboardServer | None = None
        self._stop_event = asyncio.Event()
        # Serializes start/stop so concurrent dashboard requests (or a stop
        # arriving mid-start) cannot orphan WS clients or leak eval loops.
        self._ctl_lock = asyncio.Lock()
        self._eval_interval: float = max(
            0.5,
            config.features.persistence_window_sec
            / max(config.features.persistence_windows, 1),
        )

        # Per-run state (recreated by start_trading)
        self._symbol: str = config.market.symbol
        self._commission: CommissionInfo | None = None
        self._book_state = OrderBookState()
        self._trades = TradesStream(window_sec=config.features.ofi_z_window_sec)
        self._features: FeatureEngine | None = None
        self._scorer: Scorer | None = None
        self._last_raw_score: float = 0.0
        self._edge: EdgeEstimator | None = None
        self._engine: PaperEngine | None = None
        self._maker: MakerEngine | None = None
        self._risk = RiskManager(config.risk, config.position)
        self._report: ReportWriter | None = None
        self._ws: BitpinWsClient | None = None
        self._tasks: list[asyncio.Task] = []
        self._trading = False
        self._last_status_at: float = 0.0

        # Tradable-symbol list cache for the dashboard selector
        self._symbols_cache: list[str] = []
        self._symbols_fetched_at: float = 0.0
        self._status_error: str = ""

    # ------------------------------------------------------------------
    # Status / control API (used by the dashboard server)
    # ------------------------------------------------------------------

    def status(self) -> dict[str, Any]:
        return {
            "running": self._trading,
            "symbol": self._symbol,
            "error": self._status_error,
        }

    async def symbols(self) -> list[str]:
        now = time.time()
        if (
            self._symbols_cache
            and now - self._symbols_fetched_at < _SYMBOLS_CACHE_SEC
        ):
            return self._symbols_cache
        markets = await self._rest.list_markets()
        # Capital is in IRT, so only IRT-quoted markets are tradeable here.
        symbols = sorted(
            m["symbol"]
            for m in markets
            if m.get("tradable")
            and not m.get("suspended")
            and m["symbol"].endswith("_IRT")
        )
        self._symbols_cache = symbols
        self._symbols_fetched_at = now
        return symbols

    async def start_trading(self, symbol: str | None = None) -> dict[str, Any]:
        """(Re)start the trading loop on ``symbol`` (default: current)."""
        async with self._ctl_lock:
            if self._trading:
                raise RuntimeError(
                    "Trading is already running — stop it before starting again"
                )
            try:
                status = await self._start_trading_impl(symbol)
            except Exception as exc:  # noqa: BLE001
                self._status_error = str(exc)
                self._dashboard_state.set_status(False, self._symbol, str(exc))
                await self._cleanup_failed_start()
                raise
            self._status_error = ""
            return status

    async def _cleanup_failed_start(self) -> None:
        """Tear down anything a partially-completed start left behind."""
        ws, self._ws = self._ws, None
        if ws is not None:
            try:
                await ws.stop()
            except Exception:  # noqa: BLE001
                logger.debug("WS cleanup after failed start", exc_info=True)
        for task in self._tasks:
            task.cancel()
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks = []
        self._trading = False

    async def _start_trading_impl(self, symbol: str | None) -> dict[str, Any]:
        target = (symbol or self._symbol).upper().strip()
        cfg = self._config

        logger.info("Starting trading on %s ...", target)
        market = await self._rest.get_market_info(target)
        if market.suspended:
            raise RuntimeError(
                f"Market {target} is suspended right now "
                "(e.g. USDT_IRT is closed 21:00-09:00 Tehran)"
            )
        if not market.tradable:
            raise RuntimeError(f"Market {target} is not tradable")

        try:
            commission = await self._rest.get_commission(target)
            logger.info(
                "Commission %s: maker=%.4f%% taker=%.4f%%",
                target,
                commission.maker_fraction * 100,
                commission.taker_fraction * 100,
            )
        except Exception:  # noqa: BLE001
            logger.warning(
                "Commission fetch failed; using config defaults for %s", target
            )
            commission = CommissionInfo(
                maker=cfg.edge.default_fee_maker,
                taker=cfg.edge.default_fee_taker,
            )

        snapshot = await self._rest.get_orderbook_snapshot(target)

        # Fresh per-run state
        self._symbol = target
        self._commission = commission
        self._book_state = OrderBookState()
        self._book_state.apply_rest_snapshot(snapshot)
        if not self._book_state.book.is_valid():
            raise RuntimeError(f"Initial order-book snapshot invalid for {target}")
        logger.info(
            "Initial book %s: bid=%.2f ask=%.2f spread=%.2f",
            target,
            self._book_state.book.best_bid.price,  # type: ignore[union-attr]
            self._book_state.book.best_ask.price,  # type: ignore[union-attr]
            self._book_state.book.spread,  # type: ignore[union-attr]
        )

        self._trades = TradesStream(window_sec=cfg.features.ofi_z_window_sec)
        self._features = FeatureEngine(cfg.features)
        self._scorer = Scorer(cfg.scoring)
        self._edge = EdgeEstimator(cfg.edge, cfg.execution, commission)
        self._engine = PaperEngine(cfg.capital.initial_irt, cfg.execution, commission)
        self._maker = (
            MakerEngine(
                cfg.maker,
                cfg.exit,
                commission.maker_fraction,
                commission.taker_fraction,
                cfg.paths.raw_dir,
            )
            if cfg.maker.enabled
            else None
        )
        # NOTE: self._risk is intentionally reused across (re)starts so the
        # daily-loss accumulator survives a Stop/Start within the same day.
        self._report = ReportWriter(cfg.paths.reports_dir, cfg.capital.initial_irt)
        self._ws = BitpinWsClient(
            cfg.api.ws_url,
            target,
            on_book=self._on_book,
            on_matches=self._on_matches,
        )
        try:
            await self._ws.start()
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                f"WebSocket failed to become ready for {target}: {exc}"
            ) from exc

        self._recorder.archive_signals()
        self._dashboard_state.reset_run_data()
        self._dashboard_state.set_params(
            self._build_dashboard_params(target, commission)
        )
        self._last_status_at = 0.0
        self._trading = True
        self._dashboard_state.set_status(True, target, "")

        self._tasks = [
            asyncio.create_task(self._eval_loop()),
            asyncio.create_task(self._resync_loop()),
        ]
        logger.info(
            "Trading started: symbol=%s capital=%.0f IRT eval_interval=%.2fs",
            target,
            cfg.capital.initial_irt,
            self._eval_interval,
        )
        return self.status()

    async def stop_trading(self, reason: str = "manual") -> dict[str, Any]:
        """Stop the trading loop; force-close any open paper position."""
        async with self._ctl_lock:
            if not self._trading:
                return self.status()
            logger.info("Stopping trading (%s) ...", reason)

            for task in self._tasks:
                task.cancel()
            await asyncio.gather(*self._tasks, return_exceptions=True)
            self._tasks = []

            if self._ws is not None:
                try:
                    await self._ws.stop()
                except Exception:  # noqa: BLE001
                    logger.debug("WS stop failed during stop_trading", exc_info=True)
                self._ws = None

            engine = self._engine
            report = self._report
            if engine is not None and report is not None:
                book = self._book_state.book
                trade = None
                if engine.account.state.value == "long" and book.is_valid():
                    trade = engine.try_exit_long(book, ExitReason.SHUTDOWN)
                    if trade is not None:
                        self._risk.register_realized_pnl(
                            trade.pnl_irt, time.time()
                        )
                        report.record_closed_trade(trade, engine.account)
                        logger.info(
                            "Force-closed open position on stop: pnl=%.0f IRT",
                            trade.pnl_irt,
                        )
                mark = book.best_bid.price if book.best_bid else 0.0
                maker = self._maker
                if maker is not None:
                    closed = maker.close_all(book, time.time(), reason="shutdown")
                    if closed is not None:
                        logger.info(
                            "Maker: force-closed on stop: pnl=%.0f IRT (%.1f bps)",
                            closed["pnl_irt"],
                            closed["net_bps"],
                        )
                    self._dashboard_state.sync_maker(maker)
                summary = report.write_summary(engine.account, mark_price=mark)
                report.log_summary(summary)
                logger.info("Reports written to %s", self._config.paths.reports_dir)
                # Final dashboard sync so a force-closed position does not
                # linger as a live OPEN row after trading has stopped.
                self._dashboard_state.sync_engine(engine, book, time.time())

            self._trading = False
            self._status_error = ""
            self._dashboard_state.set_status(False, self._symbol, "")
            return self.status()

    # ------------------------------------------------------------------
    # WebSocket callbacks (per-run; bound to the current WS client)
    # ------------------------------------------------------------------

    def _on_book(self, payload: dict) -> None:
        self._book_state.apply_snapshot(payload)
        self._recorder.record_book(payload)
        if self._book_state.book.is_valid():
            self._dashboard_state.on_book(self._book_state.book, time.time())
        if self._features is not None and self._book_state.book.is_valid():
            self._features.on_book(self._book_state.book)
        if self._maker is not None and self._book_state.book.is_valid():
            self._maker.on_book(self._book_state.book, time.time())

    def _on_matches(self, payload: dict) -> None:
        self._trades.apply_matches(payload)
        self._recorder.record_matches(payload)
        self._dashboard_state.on_matches(payload)
        if self._maker is not None:
            self._maker.on_matches(payload, time.time())

    # ------------------------------------------------------------------
    # Durable setup (once per process)
    # ------------------------------------------------------------------

    async def setup(self) -> None:
        cfg = self._config
        # Auth is optional for paper trading (only the commissions endpoint
        # needs it); if the IP is not whitelisted yet, fall back to defaults.
        if cfg.api.api_key and cfg.api.secret_key:
            logger.info("Authenticating with Bitpin...")
            try:
                await self._rest.authenticate()
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "Authentication failed (%s); continuing unauthenticated "
                    "(default fees will be used)",
                    exc,
                )
        else:
            logger.warning(
                "No API credentials configured; continuing unauthenticated"
            )

        if cfg.dashboard.enabled:
            self._dashboard = DashboardServer(
                self._dashboard_state,
                host=cfg.dashboard.host,
                port=cfg.dashboard.port,
                controller=self,
            )
            await self._dashboard.start()

    def _build_dashboard_params(
        self, symbol: str, commission: CommissionInfo
    ) -> dict:
        cfg = self._config
        return {
            "symbol": symbol,
            "capital_irt": cfg.capital.initial_irt,
            "eval_interval_sec": round(self._eval_interval, 2),
            "features": {
                "depth_levels": cfg.features.depth_levels,
                "depth_lambda": cfg.features.depth_lambda,
                "depth_cap_mult": cfg.features.depth_cap_mult,
                "ofi_z_window_sec": cfg.features.ofi_z_window_sec,
                "min_ofi_samples": cfg.features.min_ofi_samples,
                "persistence_windows": cfg.features.persistence_windows,
                "persistence_window_sec": cfg.features.persistence_window_sec,
            },
            "scoring": {
                "weight_depth": cfg.scoring.weight_depth,
                "weight_micro": cfg.scoring.weight_micro,
                "weight_ofi": cfg.scoring.weight_ofi,
                "ofi_scale": cfg.scoring.ofi_scale,
                "ema_half_life_sec": cfg.scoring.ema_half_life_sec,
            },
            "entry": {
                "min_score": cfg.entry.min_score,
            },
            "edge": {
                "expected_move_coef": cfg.edge.expected_move_coef,
                "required_edge": cfg.edge.required_edge,
                "enforce": cfg.edge.enforce,
            },
            "risk": {
                "stop_loss_pct": cfg.risk.stop_loss_pct,
                "take_profit_pct": cfg.risk.take_profit_pct,
                "max_daily_loss_irt": cfg.risk.max_daily_loss_irt,
                "max_spread_pct": cfg.risk.max_spread_pct,
                "book_stale_sec": cfg.risk.book_stale_sec,
            },
            "exit": {
                "score_exit_threshold": cfg.exit.score_exit_threshold,
                "max_holding_sec": cfg.exit.max_holding_sec,
                "min_hold_sec": cfg.exit.min_hold_sec,
                "score_exit_windows": cfg.exit.score_exit_windows,
            },
            "execution": {
                "max_levels_walk": cfg.execution.max_levels_walk,
                "max_slippage": cfg.execution.max_slippage,
                "edge_exit_slippage": cfg.execution.edge_exit_slippage,
            },
            "fees": {
                "maker": commission.maker_fraction,
                "taker": commission.taker_fraction,
            },
            "maker": {
                "enabled": cfg.maker.enabled,
                "min_score": cfg.maker.min_score,
                "tp_pct": cfg.maker.tp_pct,
                "stop_loss_pct": cfg.maker.stop_loss_pct,
                "entry_timeout_sec": cfg.maker.entry_timeout_sec,
                "exit_timeout_sec": cfg.maker.exit_timeout_sec,
                "max_holding_sec": cfg.maker.max_holding_sec,
                "repeg_bps": cfg.maker.repeg_bps,
            },
        }

    # ------------------------------------------------------------------
    # Periodic tasks
    # ------------------------------------------------------------------

    async def _resync_loop(self) -> None:
        """Pull a REST snapshot periodically to guard against WS gaps.

        The orderbook WS channel only pushes on change, so during quiet
        markets this resync is also what keeps the staleness gate satisfied.
        Every 4th cycle also re-checks the market's suspended flag: without
        it the bot would keep trading on a frozen book after e.g. USDT_IRT
        closes for the night (the REST resync refreshes book freshness).
        """
        interval = self._config.api.resync_interval_sec
        cycles = 0
        while self._trading:
            await asyncio.sleep(interval)
            try:
                snapshot = await self._rest.get_orderbook_snapshot(self._symbol)
                self._book_state.apply_rest_snapshot(snapshot)
                logger.debug("Order book resynced from REST")
            except Exception as exc:  # noqa: BLE001
                logger.warning("REST resync failed: %s", exc)

            cycles += 1
            if cycles % 4 == 0 and await self._market_not_tradable():
                logger.warning(
                    "Market %s is suspended/not tradable; stopping trading",
                    self._symbol,
                )
                # Stop from a separate task: stop_trading cancels this loop,
                # and awaiting it from inside itself would deadlock.
                asyncio.ensure_future(self._stop_for_suspension())
                return

    async def _market_not_tradable(self) -> bool:
        try:
            info = await self._rest.get_market_info(self._symbol)
            return info.suspended or not info.tradable
        except Exception as exc:  # noqa: BLE001
            logger.debug("Suspension check failed: %s", exc)
            return False

    async def _stop_for_suspension(self) -> None:
        try:
            await self.stop_trading("market_suspended")
        finally:
            msg = "Market suspended (e.g. USDT_IRT closes 21:00-09:00 Tehran)"
            self._status_error = msg
            self._dashboard_state.set_status(False, self._symbol, msg)

    async def _eval_loop(self) -> None:
        """Core decision loop, driven by wall clock, not by message rate."""
        while self._trading:
            await asyncio.sleep(self._eval_interval)
            try:
                self._evaluate_once()
            except Exception:  # noqa: BLE001
                logger.exception("Evaluation cycle failed")

    def _evaluate_once(self) -> None:
        features_engine = self._features
        scorer = self._scorer
        edge_estimator = self._edge
        engine = self._engine
        report = self._report
        assert (
            features_engine is not None
            and scorer is not None
            and edge_estimator is not None
            and engine is not None
            and report is not None
        )

        now = time.time()
        book = self._book_state.book
        action = "hold"

        # --- Staleness / halt handling ---
        self._risk.clear_halt_if_healthy(book, now)
        if self._risk.halted:
            self._record_signal_raw(now, action=f"halt:{self._risk.halt_reason}")
            return

        if not self._risk.book_is_tradable(book, now):
            self._record_signal_raw(now, action="skip:book_not_tradable")
            return

        # Sample equity every cycle so max drawdown captures unrealized
        # swings inside open positions, not just trade-close snapshots.
        if book.is_valid():
            report.on_mark(engine.equity_irt(book))

        # --- Features + score ---
        feats = features_engine.compute(book, now)
        score_result = scorer.compute(feats, now)
        score = score_result.score if score_result.valid else 0.0
        self._last_raw_score = score_result.raw_score if score_result.valid else 0.0

        features_engine.persistence.update(score, now)
        persistent = features_engine.persistence.is_persistent()
        dominant = features_engine.persistence.dominant_sign()

        if self._maker is not None:
            self._maker.eval(
                feats_valid=feats.valid,
                score=score if score_result.valid else None,
                persistent=persistent,
                dominant=dominant,
                book=book,
                now=now,
            )
            self._dashboard_state.sync_maker(self._maker, book, now)

        if now - self._last_status_at >= 30.0:
            self._last_status_at = now
            maker_state = (
                self._maker.payload(book, now)["state"]
                if self._maker is not None
                else "off"
            )
            logger.info(
                "status %s mid=%.0f spread=%.0f bps book_age=%.1fs score=%+.3f "
                "raw=%+.3f persistent=%s pos=%s maker=%s equity=%.0f IRT",
                self._symbol,
                feats.mid,
                feats.spread_pct * 10000 if feats.valid else -1,
                book.age_sec(now),
                score,
                self._last_raw_score,
                persistent,
                engine.account.state.value,
                maker_state,
                engine.equity_irt(book),
            )

        # --- Risk: force exit if daily loss breached while in position ---
        in_position = engine.account.state.value == "long"
        if in_position and not self._risk.daily_loss_not_breached(now):
            trade = engine.try_exit_long(book, ExitReason.MANUAL_RISK)
            if trade is not None:
                self._risk.register_realized_pnl(trade.pnl_irt, now)
                report.record_closed_trade(trade, engine.account)
                action = "exit:daily_loss"
            else:
                action = "exit_failed:daily_loss"
            self._record_signal(
                feats, score, edge_estimator, now, action, persistent, dominant
            )
            return

        # --- Exits (independent of entry logic) ---
        if in_position:
            reason = self._exits.check(engine, book, score, now)
            if reason is not None:
                trade = engine.try_exit_long(book, reason)
                if trade is not None:
                    self._risk.register_realized_pnl(trade.pnl_irt, now)
                    report.record_closed_trade(trade, engine.account)
                    action = f"exit:{reason.value}"
                else:
                    action = f"exit_failed:{reason.value}"
            else:
                action = "hold:position_open"
            self._record_signal(
                feats, score, edge_estimator, now, action, persistent, dominant
            )
            return

        # --- Entries ---
        if not feats.valid or not score_result.valid:
            self._record_signal(
                feats, score, edge_estimator, now, "skip:invalid_features",
                persistent, dominant,
            )
            return
        if dominant <= 0 or not persistent or score <= 0:
            self._record_signal(
                feats, score, edge_estimator, now, "wait:signal",
                persistent, dominant,
            )
            return
        if score < self._config.entry.min_score:
            # Too weak to pay for round-trip fees (see calibration).
            self._record_signal(
                feats, score, edge_estimator, now, "wait:min_score",
                persistent, dominant,
            )
            return

        edge = edge_estimator.estimate(feats, score)
        if not edge.valid or not edge.passes_gate:
            logger.debug(
                "Entry blocked by edge gate: net=%.6f required=%.6f",
                edge.net_edge,
                self._config.edge.required_edge,
            )
            self._record_signal(
                feats, score, edge_estimator, now, "edge_blocked",
                persistent, dominant, edge=edge,
            )
            return

        sizing = self._risk.size_entry(
            book,
            equity_irt=engine.equity_irt(book),
            cash_irt=engine.account.cash_irt,
        )
        if not sizing.allowed or sizing.quantity <= 0:
            self._record_signal(
                feats, score, edge_estimator, now,
                f"sizing:{sizing.limiting_factor}", persistent, dominant,
                edge=edge,
            )
            return

        trade = engine.try_enter_long(book, sizing.quantity, score)
        self._record_signal(
            feats, score, edge_estimator, now,
            "entered" if trade is not None else "entry_rejected",
            persistent, dominant, edge=edge,
        )

    def _record_signal(
        self,
        feats,
        score: float,
        edge_estimator: EdgeEstimator,
        now: float,
        action: str,
        persistent: bool,
        dominant: int,
        edge: Any = "auto",
    ) -> None:
        if edge == "auto":
            edge = edge_estimator.estimate(feats, score) if feats.valid else None
        self._recorder.record_signal(
            {
                "ts": now,
                "score": round(score, 6),
                "raw_score": round(self._last_raw_score, 6),
                "depth_imbalance": round(feats.depth_imbalance, 6),
                "micro_m": round(feats.micro_m, 6),
                "ofi_z": round(feats.ofi_z, 6),
                "mid": round(feats.mid, 2),
                "spread_pct": round(feats.spread_pct, 8),
                "net_edge": round(edge.net_edge, 8) if edge and edge.valid else "",
                "persistent": persistent,
                "dominant": dominant,
                "action": action,
            }
        )
        self._update_dashboard(feats, score, persistent, dominant, action, now)

    def _record_signal_raw(self, now: float, action: str) -> None:
        """Record a row even when features could not be computed."""
        self._recorder.record_signal(
            {
                "ts": now,
                "score": "",
                "raw_score": "",
                "depth_imbalance": "",
                "micro_m": "",
                "ofi_z": "",
                "mid": "",
                "spread_pct": "",
                "net_edge": "",
                "persistent": "",
                "dominant": "",
                "action": action,
            }
        )
        self._update_dashboard(None, 0.0, False, 0, action, now)

    def _update_dashboard(
        self, feats, score: float, persistent: bool, dominant: int,
        action: str, now: float,
    ) -> None:
        if self._dashboard is None or self._engine is None:
            return
        self._dashboard_state.on_eval(
            feats=feats,
            score=score,
            persistent=persistent,
            dominant=dominant,
            action=action,
            engine=self._engine,
            book=self._book_state.book,
            halted=self._risk.halted,
            halt_reason=self._risk.halt_reason or "",
            now=now,
        )

    # ------------------------------------------------------------------
    # Process lifecycle
    # ------------------------------------------------------------------

    async def run(self, duration_sec: float | None = None) -> None:
        await self.setup()

        try:
            await self.start_trading()
        except Exception as exc:  # noqa: BLE001
            logger.error(
                "Initial start failed (%s) — dashboard stays up; "
                "use Start after fixing the issue",
                exc,
            )
            self._dashboard_state.set_status(False, self._symbol, str(exc))

        deadline_task: asyncio.Task | None = None
        if duration_sec is not None:
            async def _deadline() -> None:
                await asyncio.sleep(duration_sec)
                self._stop_event.set()

            deadline_task = asyncio.create_task(_deadline())

        try:
            await self._stop_event.wait()
        except asyncio.CancelledError:
            pass
        finally:
            if deadline_task is not None:
                deadline_task.cancel()
            await asyncio.shield(self._shutdown())

    async def _shutdown(self) -> None:
        logger.info("Shutting down...")
        try:
            await self.stop_trading("shutdown")
        except Exception:  # noqa: BLE001
            logger.debug("stop_trading failed during shutdown", exc_info=True)
        if self._dashboard is not None:
            try:
                await self._dashboard.stop()
            except Exception:  # noqa: BLE001
                logger.debug("Dashboard stop failed during shutdown", exc_info=True)
        try:
            await self._rest.close()
        except Exception:  # noqa: BLE001
            logger.debug("REST close failed during shutdown", exc_info=True)

    def request_stop(self) -> None:
        self._stop_event.set()


def _acquire_instance_lock(config: Config) -> None:
    """Hold an exclusive OS lock so only one bot instance can run.

    A second instance used to wipe the first one's data files and fight
    over the dashboard port. The lock lives in data/.instance.lock and is
    released automatically when the process exits (even on crash).
    """
    global _INSTANCE_LOCK
    lock_path = config.paths.raw_dir.parent / ".instance.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    fh = open(lock_path, "a+")  # noqa: SIM115 - held open for process lifetime
    try:
        if os.name == "nt":
            import msvcrt

            fh.seek(0)
            msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        fh.close()
        raise SystemExit(
            f"Another TradeBot instance is already running (lock: {lock_path}). "
            "Stop it first (Ctrl+C in its terminal)."
        ) from None
    fh.seek(0, os.SEEK_END)
    fh.write(f"{os.getpid()}\n")
    fh.flush()
    _INSTANCE_LOCK = fh


def _clean_previous_run(config: Config) -> None:
    """Delete logs/data left by previous process runs (fresh-state policy).

    Runs before the bot (and its recorder) is constructed, so every launch
    starts from an empty raw/reports state. Only files are removed —
    .gitkeep placeholders and subdirectories are kept.

    Before the wipe, signals/trades CSVs and books/matches JSONL (gzipped)
    are archived into data/calib so multi-day calibration data survives
    restarts.
    """
    calib_dir = config.paths.raw_dir.parent / "calib"
    stamp = time.strftime("%Y%m%d_%H%M%S")
    archived = 0
    if config.paths.raw_dir.is_dir():
        for pattern in (
            "signals*.csv",
            "trades*.csv",
            "maker_trades*.csv",
            "books*.jsonl",
            "matches*.jsonl",
        ):
            for path in sorted(config.paths.raw_dir.glob(pattern)):
                if not path.is_file() or path.stat().st_size == 0:
                    continue
                try:
                    calib_dir.mkdir(parents=True, exist_ok=True)
                    if path.suffix == ".jsonl":
                        dest = calib_dir / f"{path.stem}_{stamp}.jsonl.gz"
                        with path.open("rb") as src, gzip.open(dest, "wb") as dst:
                            shutil.copyfileobj(src, dst)
                    else:
                        dest = calib_dir / f"{path.stem}_{stamp}{path.suffix}"
                        shutil.copy2(path, dest)
                    archived += 1
                except OSError:
                    logger.debug("Could not archive %s", path, exc_info=True)
    if archived:
        logger.info(
            "Archived %d previous-run file(s) to %s (kept across restarts)",
            archived,
            calib_dir,
        )

    removed = 0
    for directory in (config.paths.raw_dir, config.paths.reports_dir):
        if not directory.is_dir():
            continue
        for path in sorted(directory.iterdir()):
            if not path.is_file() or path.name.startswith("."):
                continue
            try:
                path.unlink()
                removed += 1
            except OSError:
                logger.debug("Could not remove previous-run file %s", path, exc_info=True)
    for log_file in sorted(Path.cwd().glob("*.log")):
        try:
            log_file.unlink()
            removed += 1
        except OSError:
            # e.g. still open because the process was started with shell redirect
            logger.debug("Could not remove previous log %s", log_file, exc_info=True)
    logger.info(
        "Fresh start: removed %d file(s) from previous run(s)", removed
    )


async def _amain(config_path: str, duration_sec: float | None) -> None:
    config = load_config(config_path)

    logging.basicConfig(
        level=getattr(logging, config.logging.level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    _acquire_instance_lock(config)
    _clean_previous_run(config)

    bot = TradingBot(config)

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, bot.request_stop)
        except NotImplementedError:
            # Windows: fall back to KeyboardInterrupt below.
            pass

    try:
        await bot.run(duration_sec=duration_sec)
    except KeyboardInterrupt:
        bot.request_stop()
        logger.info("Interrupted by user")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bitpin OBI paper-trading bot")
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to YAML config (default: config.yaml)",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=None,
        help="Optional run duration in seconds; runs forever if omitted",
    )
    args = parser.parse_args()
    try:
        asyncio.run(_amain(args.config, args.duration))
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        raise SystemExit(0) from None


if __name__ == "__main__":
    main()
