"""Performance metrics and CSV/JSON report writer."""

from __future__ import annotations

import csv
import json
import logging
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from tradebot.engine.paper_engine import PaperAccount, TradeRecord

logger = logging.getLogger(__name__)

TRADE_FIELDS = [
    "trade_id",
    "side",
    "entry_time",
    "entry_price",
    "quantity",
    "quote_spent",
    "fee_entry",
    "score_at_entry",
    "exit_time",
    "exit_price",
    "quote_received",
    "fee_exit",
    "exit_reason",
    "pnl_irt",
]


@dataclass
class PerformanceSummary:
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate: float = 0.0
    total_pnl_irt: float = 0.0
    total_fees_irt: float = 0.0
    avg_pnl_irt: float = 0.0
    best_trade_irt: float = 0.0
    worst_trade_irt: float = 0.0
    max_drawdown_irt: float = 0.0
    final_equity_irt: float = 0.0
    initial_capital_irt: float = 0.0
    return_pct: float = 0.0
    exit_reason_counts: dict[str, int] = field(default_factory=dict)


class ReportWriter:
    """Writes trade history and a summary after each closed trade / at end."""

    def __init__(
        self,
        reports_dir: Path,
        initial_capital_irt: float,
    ) -> None:
        self._dir = reports_dir
        self._dir.mkdir(parents=True, exist_ok=True)
        self._trades_path = self._dir / "trades.csv"
        self._summary_path = self._dir / "summary.json"
        self._initial_capital = initial_capital_irt
        self._equity_peak = initial_capital_irt
        self._max_drawdown = 0.0

    def record_closed_trade(self, trade: TradeRecord, account: PaperAccount) -> None:
        row = asdict(trade)
        row["side"] = trade.side.value
        self._append_trade_row(row)
        equity = account.cash_irt + account.base_holding * (
            trade.exit_price or trade.entry_price
        )
        self._update_drawdown(equity)
        self.write_summary(account)

    def _append_trade_row(self, row: dict) -> None:
        write_header = not self._trades_path.exists()
        with self._trades_path.open("a", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=TRADE_FIELDS)
            if write_header:
                writer.writeheader()
            writer.writerow({k: row.get(k, "") for k in TRADE_FIELDS})

    def _update_drawdown(self, equity_irt: float) -> None:
        if equity_irt > self._equity_peak:
            self._equity_peak = equity_irt
        drawdown = self._equity_peak - equity_irt
        if drawdown > self._max_drawdown:
            self._max_drawdown = drawdown

    def summarize(
        self,
        account: PaperAccount,
        mark_price: float = 0.0,
    ) -> PerformanceSummary:
        trades = account.trades
        closed = [t for t in trades if t.is_closed]
        total = len(closed)
        wins = [t for t in closed if t.pnl_irt > 0]
        losses = [t for t in closed if t.pnl_irt <= 0]
        pnls = [t.pnl_irt for t in closed]
        fees = [t.fee_entry + t.fee_exit for t in closed]

        final_equity = account.cash_irt + account.base_holding * mark_price
        reason_counts: dict[str, int] = {}
        for trade in closed:
            reason_counts[trade.exit_reason] = (
                reason_counts.get(trade.exit_reason, 0) + 1
            )

        return PerformanceSummary(
            total_trades=total,
            winning_trades=len(wins),
            losing_trades=len(losses),
            win_rate=(len(wins) / total) if total else 0.0,
            total_pnl_irt=sum(pnls),
            total_fees_irt=sum(fees),
            avg_pnl_irt=(sum(pnls) / total) if total else 0.0,
            best_trade_irt=max(pnls) if pnls else 0.0,
            worst_trade_irt=min(pnls) if pnls else 0.0,
            max_drawdown_irt=self._max_drawdown,
            final_equity_irt=final_equity,
            initial_capital_irt=self._initial_capital,
            return_pct=(
                (final_equity - self._initial_capital) / self._initial_capital
                if self._initial_capital
                else 0.0
            ),
            exit_reason_counts=reason_counts,
        )

    def write_summary(
        self,
        account: PaperAccount,
        mark_price: float | None = None,
    ) -> PerformanceSummary:
        mark = mark_price if mark_price is not None else 0.0
        summary = self.summarize(account, mark_price=mark)
        self._update_drawdown(summary.final_equity_irt)
        summary.max_drawdown_irt = self._max_drawdown

        payload = asdict(summary)
        payload["generated_at"] = time.time()
        with self._summary_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
        return summary

    def log_summary(self, summary: PerformanceSummary) -> None:
        logger.info(
            "SUMMARY trades=%d win_rate=%.1f%% pnl=%.0f IRT fees=%.0f "
            "max_dd=%.0f equity=%.0f return=%.2f%%",
            summary.total_trades,
            summary.win_rate * 100,
            summary.total_pnl_irt,
            summary.total_fees_irt,
            summary.max_drawdown_irt,
            summary.final_equity_irt,
            summary.return_pct * 100,
        )
