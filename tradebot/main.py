"""Main orchestrator: wires data, strategy, engine, and reporting.

Run with:  python -m tradebot.main [--config config.yaml]

The bot connects to Bitpin public WebSocket channels, computes the four
order-book-imbalance features, and simulates a long-only USDT/IRT strategy
against the live book. No real orders are ever placed.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import signal
import time

from tradebot.api.rest_client import BitpinRestClient
from tradebot.api.ws_client import BitpinWsClient
from tradebot.config import Config, load_config
from tradebot.data.orderbook import OrderBookState
from tradebot.data.recorder import RawDataRecorder
from tradebot.data.trades import TradesStream
from tradebot.engine.exits import ExitRules
from tradebot.engine.paper_engine import ExitReason, PaperEngine
from tradebot.engine.risk import RiskManager
from tradebot.report.metrics import ReportWriter
from tradebot.strategy.edge import EdgeEstimator
from tradebot.strategy.features import FeatureEngine
from tradebot.strategy.scoring import Scorer

logger = logging.getLogger("tradebot")


class TradingBot:
    """Single-symbol paper-trading bot."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._rest = BitpinRestClient(config)
        self._book_state = OrderBookState()
        self._trades = TradesStream(window_sec=config.features.ofi_z_window_sec)
        self._recorder = RawDataRecorder(config.paths.raw_dir)
        self._features: FeatureEngine | None = None
        self._scorer: Scorer | None = None
        self._edge: EdgeEstimator | None = None
        self._engine: PaperEngine | None = None
        self._risk = RiskManager(config.risk, config.position)
        self._exits = ExitRules(config.exit, config.risk)
        self._report: ReportWriter | None = None
        self._ws: BitpinWsClient | None = None
        self._stop_event = asyncio.Event()
        self._last_eval_at: float = 0.0
        self._last_status_at: float = 0.0
        self._last_resync_at: float = 0.0
        self._eval_interval: float = max(
            0.5, config.features.persistence_window_sec
            / max(config.features.persistence_windows, 1)
        )

    # ------------------------------------------------------------------
    # Callbacks from WebSocket (called from the asyncio loop)
    # ------------------------------------------------------------------

    def _on_book(self, payload: dict) -> None:
        self._book_state.apply_snapshot(payload)
        self._recorder.record_book(payload)
        if self._features is not None and self._book_state.book.is_valid():
            self._features.on_book(self._book_state.book)

    def _on_matches(self, payload: dict) -> None:
        self._trades.apply_matches(payload)
        self._recorder.record_matches(payload)

    # ------------------------------------------------------------------
    # Setup
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

        logger.info("Fetching market info for %s", cfg.market.symbol)
        market = await self._rest.get_market_info(cfg.market.symbol)
        if market.suspended:
            raise RuntimeError(
                f"Market {market.symbol} is suspended right now "
                "(e.g. USDT_IRT is closed overnight 21:00-09:00 Tehran)"
            )
        if not market.tradable:
            raise RuntimeError(f"Market {market.symbol} is not tradable")

        logger.info("Fetching commission for %s", cfg.market.symbol)
        try:
            commission = await self._rest.get_commission(cfg.market.symbol)
            logger.info(
                "Commission: maker=%.4f%% taker=%.4f%%",
                commission.maker_fraction * 100,
                commission.taker_fraction * 100,
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Commission fetch failed (%s); using config defaults", exc
            )
            from tradebot.api.rest_client import CommissionInfo

            commission = CommissionInfo(
                maker=cfg.edge.default_fee_maker,
                taker=cfg.edge.default_fee_taker,
            )

        logger.info("Fetching initial order-book snapshot (REST)...")
        snapshot = await self._rest.get_orderbook_snapshot(cfg.market.symbol)
        self._book_state.apply_rest_snapshot(snapshot)
        if not self._book_state.book.is_valid():
            raise RuntimeError("Initial order-book snapshot invalid")
        logger.info(
            "Initial book: bid=%.2f ask=%.2f spread=%.2f",
            self._book_state.book.best_bid.price,  # type: ignore[union-attr]
            self._book_state.book.best_ask.price,  # type: ignore[union-attr]
            self._book_state.book.spread,  # type: ignore[union-attr]
        )

        self._features = FeatureEngine(cfg.features, self._trades)
        self._scorer = Scorer(cfg.scoring)
        self._edge = EdgeEstimator(cfg.edge, cfg.execution, commission)
        self._engine = PaperEngine(
            cfg.capital.initial_irt,
            cfg.execution,
            commission,
        )
        self._report = ReportWriter(
            cfg.paths.reports_dir,
            cfg.capital.initial_irt,
        )
        self._ws = BitpinWsClient(
            cfg.api.ws_url,
            cfg.market.symbol,
            on_book=self._on_book,
            on_matches=self._on_matches,
        )

    # ------------------------------------------------------------------
    # Periodic tasks
    # ------------------------------------------------------------------

    async def _resync_loop(self) -> None:
        """Pull a REST snapshot periodically to guard against WS gaps.

        The orderbook WS channel only pushes on change, so in quiet markets
        this resync is also what keeps the staleness gate satisfied.
        """
        interval = self._config.api.resync_interval_sec
        while not self._stop_event.is_set():
            await asyncio.sleep(interval)
            try:
                snapshot = await self._rest.get_orderbook_snapshot(
                    self._config.market.symbol
                )
                self._book_state.apply_rest_snapshot(snapshot)
                logger.debug("Order book resynced from REST")
            except Exception as exc:  # noqa: BLE001
                logger.warning("REST resync failed: %s", exc)

    async def _eval_loop(self) -> None:
        """Core decision loop, driven by wall clock, not by message rate."""
        while not self._stop_event.is_set():
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

        # --- Features + score ---
        feats = features_engine.compute(book, now)
        score_result = scorer.compute(feats)
        score = score_result.score if score_result.valid else 0.0

        features_engine.persistence.update(score, now)
        persistent = features_engine.persistence.is_persistent()
        dominant = features_engine.persistence.dominant_sign()

        if now - self._last_status_at >= 30.0:
            self._last_status_at = now
            logger.info(
                "status mid=%.0f spread=%.0f bps book_age=%.1fs score=%+.3f "
                "persistent=%s pos=%s equity=%.0f IRT",
                feats.mid,
                feats.spread_pct * 10000 if feats.valid else -1,
                book.age_sec(now),
                score,
                persistent,
                engine.account.state.value,
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

        edge = edge_estimator.estimate(feats, score)
        if not edge.valid or not edge.passes_gate:
            logger.debug(
                "Entry blocked by edge gate: net=%.6f required=%.6f",
                edge.net_edge,
                self._config.edge.required_edge,
            )
            self._record_signal(
                feats, score, edge_estimator, now, "edge_blocked",
                persistent, dominant,
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
            )
            return

        trade = engine.try_enter_long(book, sizing.quantity, score)
        self._record_signal(
            feats, score, edge_estimator, now,
            "entered" if trade is not None else "entry_rejected",
            persistent, dominant,
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
    ) -> None:
        edge = edge_estimator.estimate(feats, score) if feats.valid else None
        self._recorder.record_signal(
            {
                "ts": now,
                "score": round(score, 6),
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

    def _record_signal_raw(self, now: float, action: str) -> None:
        """Record a row even when features could not be computed."""
        self._recorder.record_signal(
            {
                "ts": now,
                "score": "",
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

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def run(self, duration_sec: float | None = None) -> None:
        await self.setup()
        assert self._ws is not None and self._report is not None

        await self._ws.start()

        eval_task = asyncio.create_task(self._eval_loop())
        resync_task = asyncio.create_task(self._resync_loop())

        deadline_task: asyncio.Task | None = None
        if duration_sec is not None:
            async def _deadline() -> None:
                await asyncio.sleep(duration_sec)
                self._stop_event.set()

            deadline_task = asyncio.create_task(_deadline())

        logger.info(
            "Bot running: symbol=%s capital=%.0f IRT eval_interval=%.1fs",
            self._config.market.symbol,
            self._config.capital.initial_irt,
            self._eval_interval,
        )

        try:
            await self._stop_event.wait()
        except asyncio.CancelledError:
            pass
        finally:
            if deadline_task is not None:
                deadline_task.cancel()
            await asyncio.shield(self._shutdown(eval_task, resync_task))

    async def _shutdown(
        self,
        eval_task: asyncio.Task,
        resync_task: asyncio.Task,
    ) -> None:
        logger.info("Shutting down...")
        for task in (eval_task, resync_task):
            task.cancel()
        await asyncio.gather(eval_task, resync_task, return_exceptions=True)
        if self._ws is not None:
            try:
                await self._ws.stop()
            except Exception:  # noqa: BLE001
                logger.debug("WS stop failed during shutdown", exc_info=True)
        try:
            await self._rest.close()
        except Exception:  # noqa: BLE001
            logger.debug("REST close failed during shutdown", exc_info=True)

        engine = self._engine
        report = self._report
        if engine is not None and report is not None:
            final_book = self._book_state.book
            mark = final_book.best_bid.price if final_book.best_bid else 0.0
            summary = report.write_summary(engine.account, mark_price=mark)
            report.log_summary(summary)
            logger.info("Reports written to %s", self._config.paths.reports_dir)

    def request_stop(self) -> None:
        self._stop_event.set()


async def _amain(config_path: str, duration_sec: float | None) -> None:
    config = load_config(config_path)

    logging.basicConfig(
        level=getattr(logging, config.logging.level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

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
    asyncio.run(_amain(args.config, args.duration))


if __name__ == "__main__":
    main()
