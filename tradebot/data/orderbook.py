"""In-memory order-book state built from WebSocket snapshots.

Bitpin publishes a full top-of-book snapshot (top ~20 levels per side) on
every change; there is no sequence number, so freshness is judged purely
by wall-clock age of the last accepted snapshot.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class BookLevel:
    price: float
    volume: float


@dataclass
class OrderBook:
    """Best bid/ask plus depth arrays, ordered best-first."""

    bids: list[BookLevel] = field(default_factory=list)
    asks: list[BookLevel] = field(default_factory=list)
    last_event_time: float = 0.0
    received_at: float = 0.0

    @property
    def best_bid(self) -> BookLevel | None:
        return self.bids[0] if self.bids else None

    @property
    def best_ask(self) -> BookLevel | None:
        return self.asks[0] if self.asks else None

    @property
    def mid(self) -> float | None:
        bid = self.best_bid
        ask = self.best_ask
        if bid is None or ask is None:
            return None
        return (bid.price + ask.price) / 2.0

    @property
    def spread(self) -> float | None:
        bid = self.best_bid
        ask = self.best_ask
        if bid is None or ask is None:
            return None
        return ask.price - bid.price

    @property
    def spread_pct(self) -> float | None:
        spread = self.spread
        mid = self.mid
        if spread is None or mid is None or mid <= 0:
            return None
        return spread / mid

    def age_sec(self, now: float | None = None) -> float:
        reference = now if now is not None else time.time()
        return reference - self.received_at

    def is_fresh(self, max_age_sec: float, now: float | None = None) -> bool:
        if self.received_at <= 0:
            return False
        return self.age_sec(now) <= max_age_sec

    def is_valid(self) -> bool:
        bid = self.best_bid
        ask = self.best_ask
        if bid is None or ask is None:
            return False
        return bid.price > 0 and ask.price > 0 and bid.price < ask.price


class OrderBookState:
    """Thread-safe-ish holder; single asyncio loop so no locking needed."""

    def __init__(self) -> None:
        self.book = OrderBook()
        self.update_count = 0
        self.last_resync_at: float = 0.0

    def apply_snapshot(
        self,
        raw: dict,
        received_at: float | None = None,
    ) -> bool:
        """Parse a Bitpin payload into the live book. Returns success."""
        received = received_at if received_at is not None else time.time()
        try:
            asks = self._parse_levels(raw.get("asks"), descending=False)
            bids = self._parse_levels(raw.get("bids"), descending=True)
        except (TypeError, ValueError, KeyError):
            return False
        if not asks or not bids:
            return False

        event_ts = self._parse_event_time(raw.get("event_time") or raw.get("time"))

        self.book = OrderBook(
            bids=bids,
            asks=asks,
            last_event_time=event_ts,
            received_at=received,
        )
        self.update_count += 1
        return True

    def apply_rest_snapshot(self, raw: dict) -> bool:
        """Apply a REST snapshot used for periodic resync."""
        ok = self.apply_snapshot(raw)
        if ok:
            self.last_resync_at = time.time()
        return ok

    @staticmethod
    def _parse_event_time(value: object) -> float:
        """Exchange event_time is ISO-8601 UTC ('...Z'); time may be epoch."""
        if isinstance(value, str) and value:
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
            except ValueError:
                return 0.0
        try:
            return float(value) if value is not None else 0.0
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _parse_levels(
        raw_levels: object,
        descending: bool,
    ) -> list[BookLevel]:
        if not isinstance(raw_levels, list):
            return []
        levels: list[BookLevel] = []
        for entry in raw_levels:
            if not isinstance(entry, (list, tuple)) or len(entry) < 2:
                continue
            try:
                price = float(entry[0])
                volume = float(entry[1])
            except (TypeError, ValueError):
                continue  # one bad level must not reject the whole snapshot
            if not math.isfinite(price) or not math.isfinite(volume):
                continue
            if price <= 0 or volume <= 0:
                continue
            levels.append(BookLevel(price=price, volume=volume))
        levels.sort(key=lambda lvl: lvl.price, reverse=descending)
        return levels
