"""Independent exit rules for open paper positions."""

from __future__ import annotations

import time

from tradebot.config import ExitConfig, RiskConfig
from tradebot.data.orderbook import OrderBook
from tradebot.engine.paper_engine import ExitReason, PaperEngine


class ExitRules:
    """Decides whether an open position should be closed right now.

    Stop-loss and take-profit are immediate. The score-reversal exit is
    protected against single-eval noise by requiring both a minimum hold
    and a streak of consecutive below-threshold evaluations.
    """

    def __init__(
        self,
        exit_config: ExitConfig,
        risk_config: RiskConfig,
    ) -> None:
        self._exit = exit_config
        self._risk = risk_config
        self._streak_trade_id: str | None = None
        self._below_streak = 0

    def check(
        self,
        engine: PaperEngine,
        book: OrderBook,
        score: float | None,
        now: float | None = None,
    ) -> ExitReason | None:
        trade = engine.account.open_trade
        if trade is None:
            self._streak_trade_id = None
            self._below_streak = 0
            return None
        moment = now if now is not None else time.time()

        entry = trade.entry_price
        bid = book.best_bid
        if entry is not None and bid is not None and entry > 0:
            ret = (bid.price - entry) / entry
            if ret <= -self._risk.stop_loss_pct:
                return ExitReason.STOP_LOSS
            if ret >= self._risk.take_profit_pct:
                return ExitReason.TAKE_PROFIT

        held = moment - trade.entry_time

        if score is not None:
            if trade.trade_id != self._streak_trade_id:
                # Fresh position: reset the below-threshold streak.
                self._streak_trade_id = trade.trade_id
                self._below_streak = 0
            if score <= self._exit.score_exit_threshold:
                self._below_streak += 1
            else:
                self._below_streak = 0
            if (
                held >= self._exit.min_hold_sec
                and self._below_streak >= self._exit.score_exit_windows
            ):
                return ExitReason.SCORE_REVERSAL

        if held >= self._exit.max_holding_sec:
            return ExitReason.TIME_EXIT

        return None
