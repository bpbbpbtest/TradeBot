"""Risk manager: gates, sizing, and daily loss tracking."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from tradebot.config import PositionConfig, RiskConfig
from tradebot.data.orderbook import OrderBook

logger = logging.getLogger(__name__)


@dataclass
class SizeDecision:
    allowed: bool
    quantity: float = 0.0
    limiting_factor: str = ""


class RiskManager:
    """Central risk checks and position sizing for paper trading."""

    def __init__(
        self,
        risk_config: RiskConfig,
        position_config: PositionConfig,
    ) -> None:
        self._risk = risk_config
        self._position = position_config
        self._daily_realized_pnl: float = 0.0
        self._daily_anchor: float = self._day_start()
        self.halted: bool = False
        self.halt_reason: str = ""

    @staticmethod
    def _day_start() -> float:
        now = time.time()
        return now - (now % 86400)

    def _roll_day(self, now: float) -> None:
        if now - self._daily_anchor >= 86400:
            self._daily_anchor = self._day_start()
            self._daily_realized_pnl = 0.0
            logger.info("Daily loss counter reset")

    # ------------------------------------------------------------------
    # Gates
    # ------------------------------------------------------------------

    def book_is_tradable(self, book: OrderBook, now: float | None = None) -> bool:
        moment = now if now is not None else time.time()
        if not book.is_fresh(self._risk.book_stale_sec, moment):
            self._trigger_halt("stale_orderbook")
            return False
        if not book.is_valid():
            return False
        spread_pct = book.spread_pct
        if spread_pct is None or spread_pct > self._risk.max_spread_pct:
            logger.debug("Spread too wide: %s", spread_pct)
            return False
        return True

    def daily_loss_not_breached(self, now: float | None = None) -> bool:
        moment = now if now is not None else time.time()
        self._roll_day(moment)
        if self._daily_realized_pnl <= -self._risk.max_daily_loss_irt:
            self._trigger_halt("daily_loss_limit")
            return False
        return True

    def _trigger_halt(self, reason: str) -> None:
        if not self.halted:
            logger.warning("Risk halt triggered: %s", reason)
        self.halted = True
        self.halt_reason = reason

    def clear_halt_if_healthy(self, book: OrderBook, now: float | None = None) -> None:
        """Allow recovery once the book is fresh again (manual restart of
        daily loss halt is not automatic by design)."""
        moment = now if now is not None else time.time()
        if self.halt_reason == "stale_orderbook" and book.is_fresh(
            self._risk.book_stale_sec, moment
        ):
            self.halted = False
            self.halt_reason = ""

    # ------------------------------------------------------------------
    # Accounting hooks
    # ------------------------------------------------------------------

    def register_realized_pnl(self, pnl_irt: float, now: float | None = None) -> None:
        moment = now if now is not None else time.time()
        self._roll_day(moment)
        self._daily_realized_pnl += pnl_irt

    @property
    def daily_realized_pnl(self) -> float:
        return self._daily_realized_pnl

    # ------------------------------------------------------------------
    # Position sizing
    # ------------------------------------------------------------------

    def size_entry(
        self,
        book: OrderBook,
        equity_irt: float,
        cash_irt: float,
    ) -> SizeDecision:
        """min(cash available, equity-strategy cap, tradeable touch depth)."""
        if equity_irt <= 0 or cash_irt <= 0:
            return SizeDecision(False, limiting_factor="no_cash")

        ask = book.best_ask
        if ask is None or book.best_bid is None:
            return SizeDecision(False, limiting_factor="empty_book")

        # 1) Cash actually available right now.
        q_cash = cash_irt

        # 2) Strategy cap on exposure relative to current equity.
        q_cap = equity_irt * self._position.max_position_fraction

        # 3) Immediately tradeable depth at the touch (asks for a buy).
        touch_notional = ask.price * ask.volume
        q_liquidity = touch_notional * self._position.max_touch_depth_fraction

        factors = {
            "cash": q_cash,
            "strategy_cap": q_cap,
            "liquidity": q_liquidity,
        }
        quantity = min(factors.values())
        limiting = min(factors, key=factors.get)  # type: ignore[arg-type]

        if quantity <= 0:
            return SizeDecision(False, limiting_factor="zero_quantity")
        return SizeDecision(True, quantity=quantity, limiting_factor=limiting)
