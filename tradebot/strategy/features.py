"""Feature engineering for the order-book imbalance strategy.

Four independent features are computed from the live order book:

1. Depth imbalance  I_depth in [-1, 1]  (weighted depth, levels 2..N)
2. Microprice       M        in [-1, 1]  (best-level size imbalance)
3. Order-flow       OFI z-score          (top-of-book changes over time)
4. Persistence                               (sign stability of the score)
"""

from __future__ import annotations

import math
import statistics
import time
from collections import deque
from dataclasses import dataclass

from tradebot.config import FeatureConfig
from tradebot.data.orderbook import BookLevel, OrderBook


@dataclass
class Features:
    valid: bool = False
    depth_imbalance: float = 0.0
    micro_m: float = 0.0
    ofi_raw: float = 0.0
    ofi_z: float = 0.0
    ofi_samples: int = 0
    mid: float = 0.0
    spread: float = 0.0
    spread_pct: float = 0.0
    best_bid: float = 0.0
    best_ask: float = 0.0
    bid_volume_l1: float = 0.0
    ask_volume_l1: float = 0.0
    imbalance_reason: str = ""


class DepthImbalance:
    """Weighted depth imbalance over levels 2..N (best level skipped).

    Each level volume is capped at ``cap_mult`` x the median volume of the
    window (both sides) before weighting, so a single spoofed wall cannot
    dominate the imbalance. ``cap_mult <= 0`` disables the cap.
    """

    def __init__(self, levels: int, decay: float, cap_mult: float = 10.0) -> None:
        self._levels = max(levels, 2)
        self._decay = decay
        self._cap_mult = cap_mult

    def compute(self, book: OrderBook) -> tuple[float, float]:
        """Return (I_depth, reason). reason is empty on success."""
        buy_volumes = [lvl.volume for lvl in book.bids[1 : self._levels]]
        sell_volumes = [lvl.volume for lvl in book.asks[1 : self._levels]]
        if self._cap_mult > 0:
            window = buy_volumes + sell_volumes
            median = statistics.median(window) if window else 0.0
            cap = self._cap_mult * median
            if cap > 0:
                buy_volumes = [min(v, cap) for v in buy_volumes]
                sell_volumes = [min(v, cap) for v in sell_volumes]
        depth_buy = sum(
            self._decay**index * volume
            for index, volume in enumerate(buy_volumes)
        )
        depth_sell = sum(
            self._decay**index * volume
            for index, volume in enumerate(sell_volumes)
        )
        total = depth_buy + depth_sell
        if total <= 0:
            return 0.0, "empty_depth"
        return (depth_buy - depth_sell) / total, ""


class MicropriceSignal:
    """Normalized microprice deviation from mid, clipped to [-1, 1]."""

    @staticmethod
    def compute(book: OrderBook) -> tuple[float, float]:
        bid = book.best_bid
        ask = book.best_ask
        if bid is None or ask is None:
            return 0.0, "missing_touch"
        if bid.volume <= 0 or ask.volume <= 0:
            return 0.0, "zero_touch_volume"

        micro = (ask.price * bid.volume + bid.price * ask.volume) / (
            bid.volume + ask.volume
        )
        mid = (bid.price + ask.price) / 2.0
        half_spread = (ask.price - bid.price) / 2.0
        if mid <= 0:
            return 0.0, "nonpositive_mid"
        if half_spread <= 0:
            # Degenerate (locked) book: micro == mid, treat as balanced.
            return 0.0, ""

        raw = (micro - mid) / half_spread
        clipped = max(-1.0, min(1.0, raw))
        return clipped, ""


class OFIEstimator:
    """Order-flow imbalance from consecutive top-of-book snapshots.

    Standard multi-level OFI decomposition (Cont et al.) collapsed to the
    touch level, then z-scored against its own recent distribution so that
    quiet and volatile regimes are comparable.
    """

    def __init__(self, config: FeatureConfig) -> None:
        self._window_sec = config.ofi_z_window_sec
        self._min_samples = config.min_ofi_samples
        self._history: deque[tuple[float, float]] = deque()
        self._prev: tuple[BookLevel, BookLevel] | None = None

    def update(self, book: OrderBook, now: float | None = None) -> float:
        """Feed a snapshot; returns the instantaneous OFI value."""
        moment = now if now is not None else time.time()
        bid = book.best_bid
        ask = book.best_ask
        if bid is None or ask is None:
            self._prev = None
            return 0.0

        ofi = 0.0
        if self._prev is not None:
            prev_bid, prev_ask = self._prev
            ofi += self._level_ofi(prev_bid, bid)
            ofi -= self._level_ofi(prev_ask, ask)

        self._prev = (bid, ask)
        self._history.append((moment, ofi))
        self._prune(moment)
        return ofi

    @staticmethod
    def _level_ofi(prev: BookLevel, curr: BookLevel) -> float:
        """Signed contribution of one side's touch changes."""
        if curr.price > prev.price:
            # Aggressive replenishment / lift: new volume enters at a worse
            # (higher for bids) price; count the new resting size as inflow.
            return curr.volume
        if curr.price < prev.price:
            # Pull: previous size leaves the book.
            return -prev.volume
        return curr.volume - prev.volume

    def _prune(self, now: float) -> None:
        cutoff = now - self._window_sec
        while self._history and self._history[0][0] < cutoff:
            self._history.popleft()

    def zscore(self, now: float | None = None) -> tuple[float, float]:
        """Return (ofi_raw_recent_mean, zscore)."""
        moment = now if now is not None else time.time()
        self._prune(moment)
        if len(self._history) < self._min_samples:
            return 0.0, 0.0

        values = [ofi for _, ofi in self._history]
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = math.sqrt(variance)
        if std < 1e-12:
            return mean, 0.0
        z = (values[-1] - mean) / std
        z = max(-3.0, min(3.0, z))
        return mean, z

    @property
    def sample_count(self) -> int:
        """Number of OFI samples currently inside the z-window."""
        return len(self._history)


class SignalPersistence:
    """Requires the blended score to keep its sign over N evaluation windows."""

    def __init__(self, windows: int, window_sec: float) -> None:
        self._windows = max(windows, 1)
        self._window_sec = window_sec
        self._history: deque[tuple[float, float]] = deque()

    def update(self, score: float, now: float | None = None) -> None:
        moment = now if now is not None else time.time()
        self._history.append((moment, score))
        self._prune(moment)

    def _prune(self, now: float) -> None:
        cutoff = now - self._window_sec * self._windows
        while self._history and self._history[0][0] < cutoff:
            self._history.popleft()

    def is_persistent(self, min_abs_score: float = 0.0) -> bool:
        """True when every recent sample agrees in sign and clears the floor."""
        if len(self._history) < 2:
            return False
        floor = max(min_abs_score, 1e-9)
        signs: list[bool] = []
        for _, score in self._history:
            if abs(score) < floor:
                return False
            signs.append(score > 0)
        return all(signs) or not any(signs)

    def dominant_sign(self) -> int:
        """+1 when recent scores lean positive, -1 when negative, 0 unknown."""
        if not self._history:
            return 0
        last_signs = [1 if s > 0 else -1 for _, s in self._history]
        if all(sign > 0 for sign in last_signs):
            return 1
        if all(sign < 0 for sign in last_signs):
            return -1
        return 0


class FeatureEngine:
    """Computes all four features from the latest order book."""

    def __init__(self, config: FeatureConfig) -> None:
        self._config = config
        self._depth = DepthImbalance(
            config.depth_levels, config.depth_lambda, config.depth_cap_mult
        )
        self._micro = MicropriceSignal()
        self._ofi = OFIEstimator(config)
        self._persistence = SignalPersistence(
            config.persistence_windows,
            config.persistence_window_sec,
        )

    @property
    def ofi(self) -> OFIEstimator:
        return self._ofi

    @property
    def persistence(self) -> SignalPersistence:
        return self._persistence

    def on_book(self, book: OrderBook) -> None:
        """Feed every incoming snapshot into the OFI estimator."""
        self._ofi.update(book)

    def compute(self, book: OrderBook, now: float | None = None) -> Features:
        moment = now if now is not None else time.time()
        if not book.is_valid():
            return Features(imbalance_reason="invalid_book")

        depth, depth_reason = self._depth.compute(book)
        micro, micro_reason = self._micro.compute(book)
        ofi_mean, ofi_z = self._ofi.zscore(moment)

        mid = book.mid
        spread = book.spread
        bid = book.best_bid
        ask = book.best_ask
        assert mid is not None and spread is not None and bid and ask

        return Features(
            valid=True,
            depth_imbalance=depth,
            micro_m=micro,
            ofi_raw=ofi_mean,
            ofi_z=ofi_z,
            ofi_samples=self._ofi.sample_count,
            mid=mid,
            spread=spread,
            spread_pct=book.spread_pct or 0.0,
            best_bid=bid.price,
            best_ask=ask.price,
            bid_volume_l1=bid.volume,
            ask_volume_l1=ask.volume,
            imbalance_reason=depth_reason or micro_reason,
        )
