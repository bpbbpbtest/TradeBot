"""Paper-trading engine: simulated fills against the live book.

No real orders are sent to the exchange. Entries and exits are matched
against the current order book using a simple walk-the-book model:

*  A buy consumes ask levels from best upward until the quote budget is
   filled or the slippage cap is hit.
*  A sell consumes bid levels from best downward.
*  Fees are charged with the real commission fetched from the API.
"""

from __future__ import annotations

import logging
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum

from tradebot.api.rest_client import CommissionInfo
from tradebot.config import ExecutionConfig
from tradebot.data.orderbook import OrderBook

logger = logging.getLogger(__name__)


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


class PositionState(str, Enum):
    FLAT = "flat"
    LONG = "long"


class ExitReason(str, Enum):
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"
    SCORE_REVERSAL = "score_reversal"
    TIME_EXIT = "time_exit"
    MANUAL_RISK = "manual_risk"


@dataclass
class Fill:
    price: float
    volume: float  # base currency volume at this level


@dataclass
class TradeRecord:
    trade_id: str
    side: Side
    entry_time: float
    entry_price: float
    quantity: float  # base units filled
    quote_spent: float  # quote (IRT) spent/received at entry
    fee_entry: float
    score_at_entry: float
    exit_time: float | None = None
    exit_price: float | None = None
    quote_received: float = 0.0
    fee_exit: float = 0.0
    exit_reason: str = ""
    pnl_irt: float = 0.0

    @property
    def is_closed(self) -> bool:
        return self.exit_time is not None


@dataclass
class PaperAccount:
    cash_irt: float
    base_holding: float = 0.0  # base currency held (long only in v1)
    state: PositionState = PositionState.FLAT
    avg_entry_price: float | None = None
    open_trade: TradeRecord | None = None
    trades: list[TradeRecord] = field(default_factory=list)


class PaperEngine:
    """Simulated execution + position bookkeeping."""

    def __init__(
        self,
        initial_cash_irt: float,
        execution_config: ExecutionConfig,
        commission: CommissionInfo,
    ) -> None:
        self._exec = execution_config
        self._fee_taker = commission.taker_fraction
        self._fee_maker = commission.maker_fraction
        self.account = PaperAccount(cash_irt=initial_cash_irt)

    # ------------------------------------------------------------------
    # Valuation helpers
    # ------------------------------------------------------------------

    def equity_irt(self, book: OrderBook) -> float:
        mark = book.mid or 0.0
        return self.account.cash_irt + self.account.base_holding * mark

    # ------------------------------------------------------------------
    # Entry
    # ------------------------------------------------------------------

    def try_enter_long(
        self,
        book: OrderBook,
        budget_irt: float,
        score: float,
    ) -> TradeRecord | None:
        """Simulate an aggressive buy that walks the ask side."""
        if self.account.state != PositionState.FLAT:
            logger.debug("Entry rejected: position already open")
            return None
        if budget_irt <= 0 or not book.asks:
            return None

        mid = book.mid
        if mid is None:
            return None

        fills, quote_spent, avg_price, slippage = self._walk_asks(
            book, budget_irt
        )
        if not fills or quote_spent <= 0:
            logger.debug("Entry rejected: no ask liquidity consumed")
            return None
        if slippage > self._exec.max_slippage:
            logger.info(
                "Entry rejected: slippage %.5f > max %.5f",
                slippage,
                self._exec.max_slippage,
            )
            return None

        quantity = sum(f.volume for f in fills)
        fee = quote_spent * self._fee_taker
        now = time.time()

        trade = TradeRecord(
            trade_id=uuid.uuid4().hex[:12],
            side=Side.BUY,
            entry_time=now,
            entry_price=avg_price,
            quantity=quantity,
            quote_spent=quote_spent,
            fee_entry=fee,
            score_at_entry=score,
        )
        self.account.cash_irt -= quote_spent + fee
        self.account.base_holding += quantity
        self.account.state = PositionState.LONG
        self.account.avg_entry_price = avg_price
        self.account.open_trade = trade

        logger.info(
            "PAPER ENTRY %s qty=%.6f base @ avg=%.2f IRT (spent=%.0f fee=%.0f slip=%.4f%%)",
            trade.trade_id,
            quantity,
            avg_price,
            quote_spent,
            fee,
            slippage * 100,
        )
        return trade

    def _walk_asks(
        self,
        book: OrderBook,
        budget_irt: float,
    ) -> tuple[list[Fill], float, float, float]:
        """Consume ask levels; returns fills, quote, avg price, slip vs mid."""
        remaining = budget_irt
        fills: list[Fill] = []
        for level in book.asks[: self._exec.max_levels_walk]:
            if remaining <= 1e-9:
                break
            level_cost = level.price * level.volume
            take = min(remaining, level_cost)
            volume = take / level.price
            if volume <= 0:
                break
            fills.append(Fill(price=level.price, volume=volume))
            remaining -= take

        quote = sum(f.price * f.volume for f in fills)
        volume = sum(f.volume for f in fills)
        if volume <= 0:
            return [], 0.0, 0.0, 0.0
        avg = quote / volume
        mid = book.mid or avg
        slip = max(0.0, (avg - mid) / mid) if mid > 0 else 0.0
        return fills, quote, avg, slip

    # ------------------------------------------------------------------
    # Exit
    # ------------------------------------------------------------------

    def try_exit_long(
        self,
        book: OrderBook,
        reason: ExitReason,
    ) -> TradeRecord | None:
        """Simulate a marketable sell that walks the bid side."""
        trade = self.account.open_trade
        if trade is None or self.account.state != PositionState.LONG:
            return None
        quantity = self.account.base_holding
        if quantity <= 0 or not book.bids:
            return None

        fills, quote_received, avg_price = self._walk_bids(book, quantity)
        if not fills or quote_received <= 0:
            logger.warning("Exit could not consume any bid liquidity")
            return None

        filled_volume = sum(f.volume for f in fills)
        fee = quote_received * self._fee_taker
        now = time.time()

        trade.exit_time = now
        trade.exit_price = avg_price
        trade.quote_received = quote_received
        trade.fee_exit = fee
        trade.exit_reason = reason.value
        trade.pnl_irt = (
            quote_received
            - trade.quote_spent
            - trade.fee_entry
            - fee
        )

        self.account.cash_irt += quote_received - fee
        self.account.base_holding = max(0.0, quantity - filled_volume)
        if self.account.base_holding <= 1e-9:
            self.account.base_holding = 0.0
            self.account.state = PositionState.FLAT
            self.account.avg_entry_price = None
            self.account.open_trade = None
        self.account.trades.append(trade)

        logger.info(
            "PAPER EXIT %s reason=%s qty=%.6f @ avg=%.2f pnl=%.0f IRT",
            trade.trade_id,
            reason.value,
            filled_volume,
            avg_price,
            trade.pnl_irt,
        )
        return trade

    def _walk_bids(
        self,
        book: OrderBook,
        quantity: float,
    ) -> tuple[list[Fill], float, float]:
        remaining = quantity
        fills: list[Fill] = []
        for level in book.bids[: self._exec.max_levels_walk]:
            if remaining <= 1e-12:
                break
            take = min(remaining, level.volume)
            if take <= 0:
                break
            fills.append(Fill(price=level.price, volume=take))
            remaining -= take

        quote = sum(f.price * f.volume for f in fills)
        filled = sum(f.volume for f in fills)
        if filled <= 0:
            return [], 0.0, 0.0
        return fills, quote, quote / filled

    # ------------------------------------------------------------------
    # Mark-to-market helpers for exit rules
    # ------------------------------------------------------------------

    def unrealized_pnl_irt(self, book: OrderBook) -> float:
        trade = self.account.open_trade
        if trade is None:
            return 0.0
        bid = book.best_bid
        if bid is None:
            return 0.0
        return self.account.base_holding * bid.price - trade.quote_spent
