"""Net-edge estimation: expected move minus round-trip costs."""

from __future__ import annotations

from dataclasses import dataclass

from tradebot.api.rest_client import CommissionInfo
from tradebot.config import EdgeConfig, ExecutionConfig
from tradebot.strategy.features import Features


@dataclass
class EdgeResult:
    valid: bool = False
    expected_move: float = 0.0
    round_trip_cost: float = 0.0
    net_edge: float = 0.0
    passes_gate: bool = False


class EdgeEstimator:
    """Estimates whether the predicted move pays for fees + spread + slip."""

    def __init__(
        self,
        edge_config: EdgeConfig,
        execution_config: ExecutionConfig,
        commission: CommissionInfo,
    ) -> None:
        self._edge = edge_config
        self._execution = execution_config
        self._commission = commission

    def estimate(self, features: Features, score: float) -> EdgeResult:
        if not features.valid or abs(score) < 1e-9:
            return EdgeResult(valid=False)

        fee_entry = self._commission.taker_fraction
        fee_exit = self._commission.taker_fraction
        spread_cost = features.spread_pct
        slippage = self._execution.edge_exit_slippage
        round_trip_cost = fee_entry + fee_exit + spread_cost + slippage

        expected_move = self._edge.expected_move_coef * score
        net_edge = abs(expected_move) - round_trip_cost
        passes = net_edge >= self._edge.required_edge and expected_move > 0
        if not self._edge.enforce:
            # Calibration mode: log the edge but do not block entries.
            passes = expected_move > 0

        return EdgeResult(
            valid=True,
            expected_move=expected_move,
            round_trip_cost=round_trip_cost,
            net_edge=net_edge,
            passes_gate=passes,
        )
