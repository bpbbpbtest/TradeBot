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
    depth_component: float = 0.0
    micro_component: float = 0.0
    ofi_component: float = 0.0


class Scorer:
    """score = w_d * I_depth + w_m * M + w_o * tanh(ofi_z / scale)."""

    def __init__(self, config: ScoringConfig) -> None:
        self._config = config

    def compute(self, features: Features) -> ScoreResult:
        if not features.valid:
            return ScoreResult(valid=False)

        cfg = self._config
        depth_component = cfg.weight_depth * features.depth_imbalance
        micro_component = cfg.weight_micro * features.micro_m
        ofi_component = cfg.weight_ofi * math.tanh(
            features.ofi_z / cfg.ofi_scale
        )
        score = depth_component + micro_component + ofi_component
        return ScoreResult(
            valid=True,
            score=score,
            depth_component=depth_component,
            micro_component=micro_component,
            ofi_component=ofi_component,
        )
