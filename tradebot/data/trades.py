"""Recent public trades stream (deduplicated match tape).

The Bitpin ``matches:SYMBOL`` channel republishes a rolling window of the
last ~51 trades on every publication, so ingesting it naively duplicates
each trade many times. This stream keeps one record per trade id, stamped
with the exchange's own trade time when available.
"""

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
        self._seen: dict[str, float] = {}  # trade_id -> stamp (for dedup)

    def apply_matches(self, raw: dict, received_at: float | None = None) -> int:
        """Ingest a matches publication; returns number of NEW trades added."""
        received = received_at if received_at is not None else time.time()
        matches = raw.get("matches")
        if not isinstance(matches, list):
            return 0
        added = 0
        for item in matches:
            if not isinstance(item, dict):
                continue
            trade_id = str(item.get("id", ""))
            if trade_id and trade_id in self._seen:
                continue  # republish of an already-ingested trade
            item_time = item.get("time")
            try:
                stamp = (
                    float(item_time)
                    if item_time is not None
                    else received
                )
            except (TypeError, ValueError):
                stamp = received
            try:
                trade = PublicTrade(
                    trade_id=trade_id,
                    price=float(item["price"]),
                    base_amount=float(item["base_amount"]),
                    quote_amount=float(item.get("quote_amount", 0.0)),
                    side=str(item.get("side", "")),
                    received_at=stamp,
                )
            except (KeyError, TypeError, ValueError):
                continue
            if trade.price <= 0 or trade.base_amount <= 0:
                continue
            if trade_id:
                self._seen[trade_id] = stamp
            self._trades.append(trade)
            added += 1
        self._prune(received)
        return added

    def _prune(self, now: float) -> None:
        cutoff = now - self._window_sec
        while self._trades and self._trades[0].received_at < cutoff:
            expired = self._trades.popleft()
            if expired.trade_id:
                self._seen.pop(expired.trade_id, None)

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
