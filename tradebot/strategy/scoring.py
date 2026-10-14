"""Blend of the four features into a single signed score."""

from __future__ import annotations

import math
from dataclasses import dataclass

from tradebot.config import ScoringConfig
from tradebot.strategy.features import Features


@dataclass
class ScoreResult:
    valid: bool = False
    score: float = 0.0
    raw_score: float = 0.0
    depth_component: float = 0.0
    micro_component: float = 0.0
    ofi_component: float = 0.0


class Scorer:
    """score = w_d * I_depth + w_m * M + w_o * tanh(ofi_z / scale).

    The composite score is smoothed with an EMA of half-life
    ``ema_half_life_sec`` before it reaches persistence/entry/exit, so one
    jumpy frame cannot flip decisions. ``<= 0`` keeps the raw score.
    """

    def __init__(self, config: ScoringConfig) -> None:
        self._config = config
        self._ema_value: float | None = None
        self._ema_ts: float = 0.0

    def compute(
        self,
        features: Features,
        now: float | None = None,
    ) -> ScoreResult:
        if not features.valid:
            return ScoreResult(valid=False)

        cfg = self._config
        depth_component = cfg.weight_depth * features.depth_imbalance
        micro_component = cfg.weight_micro * features.micro_m
        ofi_component = cfg.weight_ofi * math.tanh(
            features.ofi_z / cfg.ofi_scale
        )
        raw_score = depth_component + micro_component + ofi_component

        score = raw_score
        half_life = cfg.ema_half_life_sec
        if half_life > 0 and now is not None:
            if self._ema_value is not None:
                dt = now - self._ema_ts
                if 0.0 < dt <= 60.0:
                    alpha = 1.0 - 0.5 ** (dt / half_life)
                    score = self._ema_value + alpha * (raw_score - self._ema_value)
            self._ema_value = score
            self._ema_ts = now

        return ScoreResult(
            valid=True,
            score=score,
            raw_score=raw_score,
            depth_component=depth_component,
            micro_component=micro_component,
            ofi_component=ofi_component,
        )
