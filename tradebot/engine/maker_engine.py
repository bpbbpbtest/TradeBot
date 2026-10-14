"""Paper maker engine: virtual resting-limit orders filled from public data.

Runs in parallel with the taker PaperEngine on the same signals to answer
one question: does passive execution (maker fee, no spread crossing) beat
aggressive taker execution on Bitpin USDT_IRT?

No API keys and no real orders. A resting order is simulated locally and
considered filled only when public evidence proves price traded through
our level:

* a match printed strictly better than our price -> full fill at our price;
* matches printed exactly at our price accumulate volume; the fill counts
  only once the accumulated volume covers our size (queue-ahead is assumed
  full — the conservative bound, same model as scripts/simulate_maker.py);
* book-cross backup: if the best touch moves through our level (bid drops
  below a resting buy / ask rises above a resting sell), the book itself
  proves we were hit.

Lifecycle:
  signal -> rest buy at (touch - join) -> fill (maker fee)
         -> rest sell at entry*(1+tp) (maker fee on exit)
         -> or taker flatten on stop-loss / exit-timeout / score-reversal /
            max-holding / shutdown (taker fee + slippage).
"""

from __future__ import annotations

import csv
import logging
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tradebot.config import ExitConfig, MakerConfig
from tradebot.data.orderbook import OrderBook

logger = logging.getLogger(__name__)

_TRADE_FIELDS = [
    "trade_id",
    "signal_ts",
    "entry_ts",
    "entry_price",
    "qty",
    "quote_spent",
    "fee_entry",
    "exit_ts",
    "exit_price",
    "fee_exit",
    "exit_kind",
    "pnl_irt",
    "net_bps",
    "holding_sec",
    "fill_latency_sec",
    "repeg_count",
    "score_at_entry",
]

_write_errors = 0


@dataclass
class WorkingOrder:
    side: str  # "buy" | "sell"
    price: float
    qty: float
    placed_at: float
    kind: str  # "entry" | "exit"
    cum_vol: float = 0.0
    repeg_count: int = 0


@dataclass
class MakerPosition:
    entry_price: float
    qty: float
    entry_time: float
    fee_entry: float
    quote_spent: float
    signal_ts: float
    score_at_entry: float | None
    fill_latency_sec: float
    repeg_count: int = 0
    exit_order: WorkingOrder = field(default=None)  # type: ignore[assignment]


class MakerEngine:
    """Virtual maker execution driven by the same feeds as the taker engine."""

    def __init__(
        self,
        maker_cfg: MakerConfig,
        exit_cfg: ExitConfig,
        fee_maker: float,
        fee_taker: float,
        raw_dir: Path,
    ) -> None:
        self._cfg = maker_cfg
        self._fee_maker = fee_maker
        self._fee_taker = fee_taker
        self._score_exit_threshold = exit_cfg.score_exit_threshold
        self._min_hold_sec = exit_cfg.min_hold_sec
        self._score_exit_windows = exit_cfg.score_exit_windows

        self._working: WorkingOrder | None = None
        self._position: MakerPosition | None = None
        self._cool_until = 0.0
        self._below_streak = 0
        self._trade_seq = 0

        self._realized_irt = 0.0
        self._fees_irt = 0.0
        self._wins = 0
        self._closed = 0
        self._bps_sum = 0.0
        self._trades: deque[dict[str, Any]] = deque(maxlen=100)

        raw_dir.mkdir(parents=True, exist_ok=True)
        self._csv_path = raw_dir / "maker_trades.csv"
        self._csv_initialized = False
        if self._csv_path.exists():
            self._csv_path.rename(self._archive_path(raw_dir))
        logger.info(
            "Maker engine ON: tp=%.2f%% sl=%.2f%% entry_timeout=%.0fs "
            "exit_timeout=%.0fs fees maker=%.2f%%/taker=%.2f%%",
            maker_cfg.tp_pct * 100,
            maker_cfg.stop_loss_pct * 100,
            maker_cfg.entry_timeout_sec,
            maker_cfg.exit_timeout_sec,
            fee_maker * 100,
            fee_taker * 100,
        )

    @staticmethod
    def _archive_path(raw_dir: Path) -> Path:
        stamp = time.strftime("%Y%m%d_%H%M%S")
        candidate = raw_dir / f"maker_trades_{stamp}.csv"
        counter = 1
        while candidate.exists():
            candidate = raw_dir / f"maker_trades_{stamp}_{counter}.csv"
            counter += 1
        return candidate

    # ------------------------------------------------------------------
    # Public feeds
    # ------------------------------------------------------------------

    def on_matches(self, payload: dict[str, Any], now: float | None = None) -> None:
        moment = now if now is not None else time.time()
        matches = payload.get("matches")
        if not isinstance(matches, list):
            return
        for item in matches:
            if not isinstance(item, dict):
                continue
            try:
                price = float(item.get("price", 0.0))
                vol = float(item.get("base_amount", 0.0))
            except (TypeError, ValueError):
                continue
            if price <= 0 or vol <= 0:
                continue
            self._process_match(price, vol, moment)

    def on_book(self, book: OrderBook, now: float | None = None) -> None:
        moment = now if now is not None else time.time()
        if not book.is_valid():
            return
        working = self._working
        bid = book.best_bid.price if book.best_bid else None
        ask = book.best_ask.price if book.best_ask else None
        if working is not None and bid is not None and ask is not None:
            crossed = (
                bid < working.price if working.side == "buy" else ask > working.price
            )
            if crossed:
                if working.kind == "entry":
                    self._fill_entry(working.price, working.qty, moment)
                else:
                    self._fill_exit(working.price, working.qty, moment)

    # ------------------------------------------------------------------
    # Eval-cycle logic (called every eval tick from main)
    # ------------------------------------------------------------------

    def eval(
        self,
        *,
        feats_valid: bool,
        score: float | None,
        persistent: bool,
        dominant: int,
        book: OrderBook,
        now: float,
    ) -> str:
        """Advance order/position state; returns a short action label."""
        if not feats_valid or not book.is_valid():
            return "maker:skip"

        if self._position is not None:
            return self._manage_position(score, book, now)

        if self._working is not None:
            return self._manage_working(book, now)

        if now < self._cool_until:
            return "maker:cooling"

        if (
            persistent
            and dominant > 0
            and score is not None
            and score >= self._cfg.min_score
        ):
            return self._place_entry(book, now, score)
        return "maker:idle"

    def close_all(
        self, book: OrderBook, now: float | None = None, reason: str = "shutdown"
    ) -> dict[str, Any] | None:
        """Cancel working order and force-close the position at taker."""
        moment = now if now is not None else time.time()
        self._working = None
        if self._position is None:
            return None
        return self._flatten_taker(book, moment, reason)

    # ------------------------------------------------------------------
    # Internals: entries
    # ------------------------------------------------------------------

    def _place_entry(self, book: OrderBook, now: float, score: float) -> str:
        bid = book.best_bid
        if bid is None or bid.price <= 0:
            return "maker:no_bid"
        price = bid.price * (1 - self._cfg.join_offset_bps / 1e4)
        qty = self._cfg.size_quote_irt / price
        if qty <= 0:
            return "maker:zero_qty"
        self._working = WorkingOrder(
            side="buy", price=price, qty=qty, placed_at=now, kind="entry"
        )
        return "maker:resting_entry"

    def _manage_working(self, book: OrderBook, now: float) -> str:
        working = self._working
        assert working is not None
        if now - working.placed_at >= self._cfg.entry_timeout_sec:
            # One signal episode, one entry window: cool down for the same
            # period so a persistent signal cannot park a bid forever.
            self._working = None
            self._cool_until = now + self._cfg.entry_timeout_sec
            return "maker:entry_timeout"
        bid = book.best_bid
        if bid is not None and bid.price > 0:
            drift_bps = abs(bid.price - working.price) / working.price * 1e4
            if drift_bps > self._cfg.repeg_bps:
                working.price = bid.price * (1 - self._cfg.join_offset_bps / 1e4)
                working.cum_vol = 0.0
                working.repeg_count += 1
                return "maker:repeg"
        return "maker:resting_entry"

    # ------------------------------------------------------------------
    # Internals: positions and exits
    # ------------------------------------------------------------------

    def _manage_position(self, score: float | None, book: OrderBook, now: float) -> str:
        position = self._position
        assert position is not None
        if position.score_at_entry is None and score is not None:
            position.score_at_entry = score
        bid = book.best_bid
        if bid is None or bid.price <= 0:
            return "maker:hold"
        ret = (bid.price - position.entry_price) / position.entry_price
        if ret <= -self._cfg.stop_loss_pct:
            trade = self._flatten_taker(book, now, "stop_loss")
            return "maker:exit:stop_loss" if trade else "maker:exit_failed:stop_loss"

        held = now - position.entry_time
        if held >= self._cfg.max_holding_sec:
            trade = self._flatten_taker(book, now, "timeout")
            return "maker:exit:timeout" if trade else "maker:exit_failed:timeout"

        if score is not None:
            if score <= self._score_exit_threshold:
                self._below_streak += 1
            else:
                self._below_streak = 0
            if (
                held >= self._min_hold_sec
                and self._below_streak >= self._score_exit_windows
            ):
                trade = self._flatten_taker(book, now, "score_reversal")
                return (
                    "maker:exit:score_reversal" if trade else "maker:exit_failed"
                )

        working = position.exit_order
        if working is not None and now - working.placed_at >= self._cfg.exit_timeout_sec:
            trade = self._flatten_taker(book, now, "exit_timeout")
            return "maker:exit:exit_timeout" if trade else "maker:exit_failed"

        return "maker:long"

    # ------------------------------------------------------------------
    # Fill processing
    # ------------------------------------------------------------------

    def _process_match(self, price: float, vol: float, now: float) -> None:
        working = self._working
        if working is not None:
            if working.side == "buy":
                if price < working.price:
                    self._fill_entry(working.price, working.qty, now)
                elif price == working.price:
                    working.cum_vol += vol
                    if working.cum_vol >= working.qty:
                        self._fill_entry(working.price, working.qty, now)
            # sell working orders only exist as position exits (below)
        position = self._position
        if position is None:
            return
        exit_order = position.exit_order
        if exit_order is None:
            return
        if price > exit_order.price:
            self._fill_exit(exit_order.price, exit_order.qty, now)
        elif price == exit_order.price:
            exit_order.cum_vol += vol
            if exit_order.cum_vol >= exit_order.qty:
                self._fill_exit(exit_order.price, exit_order.qty, now)

    def _fill_entry(self, price: float, qty: float, now: float) -> None:
        working = self._working
        if working is None or working.kind != "entry":
            return
        self._working = None
        quote_spent = price * qty
        fee = quote_spent * self._fee_maker
        latency = now - working.placed_at
        position = MakerPosition(
            entry_price=price,
            qty=qty,
            entry_time=now,
            fee_entry=fee,
            quote_spent=quote_spent,
            signal_ts=working.placed_at,
            score_at_entry=None,
            fill_latency_sec=latency,
            repeg_count=working.repeg_count,
            exit_order=WorkingOrder(
                side="sell",
                price=price * (1 + self._cfg.tp_pct),
                qty=qty,
                placed_at=now,
                kind="exit",
            ),
        )
        # Signal score is attached by the next eval via eval(); keep None
        # until then. Signal ts == placed_at is a good approximation.
        self._position = position
        logger.info(
            "Maker ENTRY filled: price=%.2f qty=%.4f fee=%.0f IRT "
            "(rested %.1fs, repeg=%d)",
            price,
            qty,
            fee,
            latency,
            working.repeg_count,
        )

    def _fill_exit(self, price: float, qty: float, now: float) -> None:
        position = self._position
        if position is None or position.exit_order is None:
            return
        fee = price * qty * self._fee_maker
        trade = self._close_trade(price, qty, fee, "maker_tp", now)
        if trade is not None:
            logger.info(
                "Maker EXIT (maker_tp): price=%.2f pnl=%.0f IRT (%.1f bps)",
                price,
                trade["pnl_irt"],
                trade["net_bps"],
            )

    def _flatten_taker(self, book: OrderBook, now: float, reason: str) -> dict[str, Any] | None:
        position = self._position
        if position is None:
            return None
        bid = book.best_bid
        if bid is None or bid.price <= 0:
            return None
        price = bid.price * (1 - self._cfg.flatten_slippage)
        qty = position.qty
        fee = price * qty * self._fee_taker
        trade = self._close_trade(price, qty, fee, reason, now)
        if trade is not None:
            logger.info(
                "Maker EXIT (taker/%s): price=%.2f pnl=%.0f IRT (%.1f bps)",
                reason,
                price,
                trade["pnl_irt"],
                trade["net_bps"],
            )
        return trade

    def _close_trade(
        self, exit_price: float, qty: float, fee_exit: float, kind: str, now: float
    ) -> dict[str, Any] | None:
        position = self._position
        if position is None:
            return None
        self._position = None
        self._trade_seq += 1
        quote_out = exit_price * qty
        pnl = (
            quote_out
            - position.quote_spent
            - position.fee_entry
            - fee_exit
        )
        notional = position.quote_spent
        net_bps = pnl / notional * 1e4 if notional > 0 else 0.0
        holding = now - position.entry_time
        row = {
            "trade_id": f"M{self._trade_seq}",
            "signal_ts": round(position.signal_ts, 3),
            "entry_ts": round(position.entry_time, 3),
            "entry_price": round(position.entry_price, 2),
            "qty": round(qty, 6),
            "quote_spent": round(position.quote_spent, 2),
            "fee_entry": round(position.fee_entry, 2),
            "exit_ts": round(now, 3),
            "exit_price": round(exit_price, 2),
            "fee_exit": round(fee_exit, 2),
            "exit_kind": kind,
            "pnl_irt": round(pnl, 2),
            "net_bps": round(net_bps, 2),
            "holding_sec": round(holding, 1),
            "fill_latency_sec": round(position.fill_latency_sec, 1),
            "repeg_count": position.repeg_count,
            "score_at_entry": (
                round(position.score_at_entry, 4)
                if position.score_at_entry is not None
                else "",
            ),
        }
        self._append_csv(row)
        self._trades.append(row)
        self._realized_irt += pnl
        self._fees_irt += position.fee_entry + fee_exit
        self._closed += 1
        if pnl > 0:
            self._wins += 1
        self._bps_sum += net_bps
        self._below_streak = 0
        return row

    # ------------------------------------------------------------------
    # Dashboard payload
    # ------------------------------------------------------------------

    def payload(self, book: OrderBook | None = None, now: float | None = None) -> dict[str, Any]:
        moment = now if now is not None else time.time()
        working = self._working
        position = self._position
        state = "flat"
        if position is not None:
            state = "long"
        elif working is not None:
            state = "entry_working"

        working_payload = None
        if working is not None:
            working_payload = {
                "side": working.side,
                "price": round(working.price, 2),
                "qty": round(working.qty, 4),
                "age_sec": round(moment - working.placed_at, 1),
                "cum_vol": round(working.cum_vol, 4),
                "repeg_count": working.repeg_count,
            }

        position_payload = None
        if position is not None:
            bid = book.best_bid.price if book is not None and book.best_bid else None
            u_gross = (bid - position.entry_price) * position.qty if bid else None
            u_net = (
                round(bid * position.qty * (1 - self._fee_taker) - position.quote_spent - position.fee_entry, 2)
                if bid
                else None
            )
            exit_order = position.exit_order
            position_payload = {
                "entry_price": round(position.entry_price, 2),
                "qty": round(position.qty, 4),
                "entry_time": round(position.entry_time, 1),
                "holding_sec": round(moment - position.entry_time, 1),
                "u_gross": round(u_gross, 2) if u_gross is not None else None,
                "u_net": u_net,
                "exit_price": round(exit_order.price, 2) if exit_order else None,
                "exit_age_sec": (
                    round(moment - exit_order.placed_at, 1) if exit_order else None
                ),
                "dist_target_bps": (
                    round((exit_order.price - bid) / bid * 1e4, 1)
                    if exit_order and bid
                    else None
                ),
                "dist_stop_bps": (
                    round(
                        (bid - position.entry_price * (1 - self._cfg.stop_loss_pct))
                        / bid
                        * 1e4,
                        1,
                    )
                    if bid
                    else None
                ),
            }

        return {
            "enabled": True,
            "state": state,
            "working": working_payload,
            "position": position_payload,
            "stats": {
                "trades": self._closed,
                "wins": self._wins,
                "win_rate_pct": round(self._wins / self._closed * 100, 1)
                if self._closed
                else None,
                "realized_irt": round(self._realized_irt, 2),
                "fees_irt": round(self._fees_irt, 2),
                "avg_net_bps": round(self._bps_sum / self._closed, 1)
                if self._closed
                else None,
            },
            "last_trades": list(self._trades)[-10:][::-1],
        }

    # ------------------------------------------------------------------
    # CSV
    # ------------------------------------------------------------------

    def _append_csv(self, row: dict[str, Any]) -> None:
        global _write_errors
        write_header = not self._csv_initialized
        try:
            with self._csv_path.open("a", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle, fieldnames=_TRADE_FIELDS, extrasaction="ignore"
                )
                if write_header:
                    writer.writeheader()
                writer.writerow(row)
                self._csv_initialized = True
        except OSError:
            _write_errors += 1
            if _write_errors <= 5:
                logger.warning("Maker CSV write failed for %s", self._csv_path.name)
