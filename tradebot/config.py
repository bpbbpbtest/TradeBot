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
    depth_cap_mult: float = 10.0


@dataclass(frozen=True)
class ScoringConfig:
    weight_depth: float
    weight_micro: float
    weight_ofi: float
    ofi_scale: float
    ema_half_life_sec: float = 15.0


@dataclass(frozen=True)
class EdgeConfig:
    expected_move_coef: float
    required_edge: float
    default_fee_taker: float
    default_fee_maker: float
    # Safe default is calibration mode: an omitted key must never silently
    # switch on a gate that (with today's costs) blocks every entry.
    enforce: bool = False


@dataclass(frozen=True)
class ExecutionConfig:
    max_levels_walk: int
    max_slippage: float
    edge_exit_slippage: float


@dataclass(frozen=True)
class PositionConfig:
    max_position_fraction: float
    max_touch_depth_fraction: float
    # Absolute per-trade notional cap (IRT). When > 0 it replaces the
    # equity-fraction strategy cap so trade size stays fixed regardless of
    # equity drift. Cash and touch-depth limits still apply.
    max_notional_irt: float = 0.0


@dataclass(frozen=True)
class RiskConfig:
    stop_loss_pct: float
    take_profit_pct: float
    max_daily_loss_irt: float
    max_spread_pct: float
    book_stale_sec: float


@dataclass(frozen=True)
class EntryConfig:
    min_score: float


@dataclass(frozen=True)
class ExitConfig:
    score_exit_threshold: float
    max_holding_sec: float
    min_hold_sec: float = 60.0
    score_exit_windows: int = 3


@dataclass(frozen=True)
class MakerConfig:
    """Virtual resting-limit (maker) execution, run in parallel to taker.

    Fills are simulated from public book/matches data; no real orders.
    Defaults assume Bitpin level-1 fees (maker 0.30% / taker 0.35%) and the
    fee-hurdle take-profit (>=70 bps round trip plus edge).
    """

    enabled: bool = True
    min_score: float = 0.15
    join_offset_bps: float = 0.0
    # Re-peg the resting order when the touch moves further than this.
    repeg_bps: float = 5.0
    entry_timeout_sec: float = 60.0
    tp_pct: float = 0.009
    exit_timeout_sec: float = 300.0
    max_holding_sec: float = 1800.0
    stop_loss_pct: float = 0.01
    size_quote_irt: float = 950000.0
    flatten_slippage: float = 0.0005


@dataclass(frozen=True)
class PathsConfig:
    raw_dir: Path
    reports_dir: Path


@dataclass(frozen=True)
class LoggingConfig:
    level: str


@dataclass(frozen=True)
class DashboardConfig:
    enabled: bool = True
    host: str = "127.0.0.1"
    port: int = 8765
    history_max_points: int = 2000


@dataclass(frozen=True)
class Config:
    market: MarketConfig
    capital: CapitalConfig
    api: ApiConfig
    features: FeatureConfig
    scoring: ScoringConfig
    entry: EntryConfig
    edge: EdgeConfig
    execution: ExecutionConfig
    position: PositionConfig
    risk: RiskConfig
    exit: ExitConfig
    maker: MakerConfig
    paths: PathsConfig
    logging: LoggingConfig
    dashboard: DashboardConfig


def _section(raw: dict[str, Any], key: str) -> dict[str, Any]:
    value = raw.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"Missing or invalid config section: {key}")
    return value


def _build(dc_type: type, section: dict[str, Any], name: str) -> Any:
    """Instantiate a config dataclass, reporting bad keys clearly."""
    try:
        return dc_type(**section)
    except TypeError as exc:
        raise ValueError(f"Invalid config section '{name}': {exc}") from exc


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

    # Paper trading works without auth (public market data only); the bot
    # logs a warning and falls back to configured default fees.
    api_key = os.environ.get("BITPIN_API_KEY", "")
    secret_key = os.environ.get("BITPIN_SECRET_KEY", "")

    paths = _section(raw, "paths")
    try:
        raw_dir = Path(paths["raw_dir"])
        reports_dir = Path(paths["reports_dir"])
    except KeyError as exc:
        raise ValueError(f"Missing key in config section 'paths': {exc}") from exc
    # Resolve data paths against the config file's directory so running the
    # bot from another working directory cannot record elsewhere or wipe an
    # unrelated ./data/raw (see main._clean_previous_run).
    base_dir = path.resolve().parent
    if not raw_dir.is_absolute():
        raw_dir = base_dir / raw_dir
    if not reports_dir.is_absolute():
        reports_dir = base_dir / reports_dir

    dashboard_raw = raw.get("dashboard")
    if dashboard_raw is None:
        dashboard_raw = {}
    elif not isinstance(dashboard_raw, dict):
        raise ValueError("Missing or invalid config section: dashboard")

    maker_raw = raw.get("maker")
    if maker_raw is None:
        maker_raw = {}
    elif not isinstance(maker_raw, dict):
        raise ValueError("Missing or invalid config section: maker")

    return Config(
        market=_build(MarketConfig, _section(raw, "market"), "market"),
        capital=_build(CapitalConfig, _section(raw, "capital"), "capital"),
        api=_build(
            ApiConfig,
            {**_section(raw, "api"), "api_key": api_key, "secret_key": secret_key},
            "api",
        ),
        features=_build(FeatureConfig, _section(raw, "features"), "features"),
        scoring=_build(ScoringConfig, _section(raw, "scoring"), "scoring"),
        entry=_build(EntryConfig, _section(raw, "entry"), "entry"),
        edge=_build(EdgeConfig, _section(raw, "edge"), "edge"),
        execution=_build(ExecutionConfig, _section(raw, "execution"), "execution"),
        position=_build(PositionConfig, _section(raw, "position"), "position"),
        risk=_build(RiskConfig, _section(raw, "risk"), "risk"),
        exit=_build(ExitConfig, _section(raw, "exit"), "exit"),
        maker=_build(MakerConfig, maker_raw, "maker"),
        paths=PathsConfig(raw_dir=raw_dir, reports_dir=reports_dir),
        logging=_build(LoggingConfig, _section(raw, "logging"), "logging"),
        dashboard=_build(DashboardConfig, dashboard_raw, "dashboard"),
    )
