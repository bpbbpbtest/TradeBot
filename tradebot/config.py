"""Configuration loading and typed access."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


@dataclass(frozen=True)
class MarketConfig:
    symbol: str


@dataclass(frozen=True)
class CapitalConfig:
    initial_irt: float


@dataclass(frozen=True)
class ApiConfig:
    base_url: str
    ws_url: str
    api_key: str
    secret_key: str
    timeout_sec: float
    resync_interval_sec: float = 15.0


@dataclass(frozen=True)
class FeatureConfig:
    depth_levels: int
    depth_lambda: float
    ofi_z_window_sec: float
    min_ofi_samples: int
    persistence_windows: int
    persistence_window_sec: float


@dataclass(frozen=True)
class ScoringConfig:
    weight_depth: float
    weight_micro: float
    weight_ofi: float
    ofi_scale: float


@dataclass(frozen=True)
class EdgeConfig:
    expected_move_coef: float
    required_edge: float
    default_fee_taker: float
    default_fee_maker: float
    enforce: bool = True


@dataclass(frozen=True)
class ExecutionConfig:
    max_levels_walk: int
    max_slippage: float
    edge_exit_slippage: float


@dataclass(frozen=True)
class PositionConfig:
    max_position_fraction: float
    max_touch_depth_fraction: float


@dataclass(frozen=True)
class RiskConfig:
    stop_loss_pct: float
    take_profit_pct: float
    max_daily_loss_irt: float
    max_spread_pct: float
    book_stale_sec: float


@dataclass(frozen=True)
class ExitConfig:
    score_exit_threshold: float
    max_holding_sec: float


@dataclass(frozen=True)
class PathsConfig:
    raw_dir: Path
    reports_dir: Path


@dataclass(frozen=True)
class LoggingConfig:
    level: str


@dataclass(frozen=True)
class Config:
    market: MarketConfig
    capital: CapitalConfig
    api: ApiConfig
    features: FeatureConfig
    scoring: ScoringConfig
    edge: EdgeConfig
    execution: ExecutionConfig
    position: PositionConfig
    risk: RiskConfig
    exit: ExitConfig
    paths: PathsConfig
    logging: LoggingConfig


def _section(raw: dict[str, Any], key: str) -> dict[str, Any]:
    value = raw.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"Missing or invalid config section: {key}")
    return value


def load_config(config_path: str | Path = "config.yaml") -> Config:
    """Load YAML config plus API credentials from the environment (.env)."""
    load_dotenv()

    path = Path(config_path)
    if not path.is_file():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    if not isinstance(raw, dict):
        raise ValueError("Config root must be a mapping")

    api_key = os.environ.get("BITPIN_API_KEY", "")
    secret_key = os.environ.get("BITPIN_SECRET_KEY", "")
    if not api_key or not secret_key:
        # Paper trading works without auth (public market data only); the
        # bot logs a warning and falls back to configured default fees.
        api_key = api_key or ""
        secret_key = secret_key or ""

    paths = _section(raw, "paths")
    return Config(
        market=MarketConfig(**_section(raw, "market")),
        capital=CapitalConfig(**_section(raw, "capital")),
        api=ApiConfig(
            **_section(raw, "api"),
            api_key=api_key,
            secret_key=secret_key,
        ),
        features=FeatureConfig(**_section(raw, "features")),
        scoring=ScoringConfig(**_section(raw, "scoring")),
        edge=EdgeConfig(**_section(raw, "edge")),
        execution=ExecutionConfig(**_section(raw, "execution")),
        position=PositionConfig(**_section(raw, "position")),
        risk=RiskConfig(**_section(raw, "risk")),
        exit=ExitConfig(**_section(raw, "exit")),
        paths=PathsConfig(
            raw_dir=Path(paths["raw_dir"]),
            reports_dir=Path(paths["reports_dir"]),
        ),
        logging=LoggingConfig(**_section(raw, "logging")),
    )
