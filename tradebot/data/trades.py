"""Recent public trades stream used by the OFI/persistence features."""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class PublicTrade:
    trade_id: str
    price: float
    base_amount: float
    quote_amount: float
    side: str
    received_at: float


class TradesStream:
    """Keeps a time window of public matches for one symbol."""

    def __init__(self, window_sec: float = 120.0) -> None:
        self._window_sec = window_sec
        self._trades: deque[PublicTrade] = deque()

    def apply_matches(self, raw: dict, received_at: float | None = None) -> int:
        """Ingest a matches publication; returns number of trades added."""
        received = received_at if received_at is not None else time.time()
        matches = raw.get("matches")
        if not isinstance(matches, list):
            return 0
        added = 0
        for item in matches:
            if not isinstance(item, dict):
                continue
            try:
                trade = PublicTrade(
                    trade_id=str(item.get("id", "")),
                    price=float(item["price"]),
                    base_amount=float(item["base_amount"]),
                    quote_amount=float(item.get("quote_amount", 0.0)),
                    side=str(item.get("side", "")),
                    received_at=received,
                )
            except (KeyError, TypeError, ValueError):
                continue
            if trade.price <= 0 or trade.base_amount <= 0:
                continue
            self._trades.append(trade)
            added += 1
        self._prune(received)
        return added

    def _prune(self, now: float) -> None:
        cutoff = now - self._window_sec
        while self._trades and self._trades[0].received_at < cutoff:
            self._trades.popleft()

    def recent(self, window_sec: float, now: float | None = None) -> list[PublicTrade]:
        reference = now if now is not None else time.time()
        cutoff = reference - window_sec
        return [t for t in self._trades if t.received_at >= cutoff]

    def net_base_flow(self, window_sec: float, now: float | None = None) -> float:
        """Signed base-quantity flow: buys positive, sells negative."""
        total = 0.0
        for trade in self.recent(window_sec, now):
            if trade.side == "buy":
                total += trade.base_amount
            elif trade.side == "sell":
                total -= trade.base_amount
        return total
