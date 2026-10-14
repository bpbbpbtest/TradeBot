"""Calibrate expected move vs. OBI score from recorded signal rows.

Loads every data/raw/signals*.csv produced by paper runs, computes the
forward mid-price move at several horizons for each valid eval row, and
reports expectancy net of round-trip costs (taker and maker scenarios).

Usage:
    .venv/Scripts/python.exe scripts/calibrate_edge.py [--min-n N]
"""

from __future__ import annotations

import argparse
import bisect
import csv
import glob
import math
import statistics
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from tradebot.config import load_config  # noqa: E402

# Current run (data/raw) + preserved archive (data/calib), anchored to the
# repo so the script works from any working directory.
RAW_GLOB = str(_REPO_ROOT / "data" / "*" / "signals*.csv")
HORIZONS = (5, 15, 30, 60, 90, 120, 180, 300, 600, 900)
SCORE_BUCKETS = (
    (0.00, 0.10),
    (0.10, 0.20),
    (0.20, 0.30),
    (0.30, 0.40),
    (0.40, 0.60),
    (0.60, 1.01),
)
# Rows recorded while already in a position / exiting are not entry signals;
# including them biases the score->move relation toward in-position periods.
_EXCLUDED_ACTIONS = ("hold:position_open", "exit:", "exit_failed:", "halt:")
DISPLAY_MIN_N = 5  # exploratory threshold for tables 1/2 (table 3 uses --min-n)


def load_rows(pattern: str) -> tuple[list[dict], int, int]:
    rows: list[dict] = []
    skipped_files = 0
    skipped_rows = 0
    for path in sorted(glob.glob(pattern)):
        with open(path, newline="") as fh:
            reader = csv.DictReader(fh)
            cols = reader.fieldnames or []
            if not {"ts", "score", "mid", "persistent"} <= set(cols):
                skipped_files += 1
                continue
            for r in reader:
                try:
                    ts = float(r["ts"])
                    score = float(r["score"])
                    mid = float(r["mid"])
                    spread = float(r["spread_pct"]) if r.get("spread_pct") else 0.0
                except (TypeError, ValueError):
                    skipped_rows += 1
                    continue
                if r["persistent"] not in ("True", "False"):
                    continue  # halt/stale rows carry no valid features
                action = (r.get("action") or "").strip()
                if action.startswith(_EXCLUDED_ACTIONS):
                    skipped_rows += 1
                    continue
                rows.append(
                    {
                        "file": path,
                        "ts": ts,
                        "score": score,
                        "mid": mid,
                        "spread_bps": spread * 1e4,
                        "persistent": r["persistent"] == "True",
                    }
                )
    return rows, skipped_files, skipped_rows


def fmt(x: float) -> str:
    return "   n/a  " if math.isnan(x) else f"{x:+8.2f}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-n", type=int, default=25, help="min samples to quote a cell")
    parser.add_argument("--pattern", default=RAW_GLOB)
    parser.add_argument(
        "--fee-taker-bps", type=float, default=None,
        help="round-trip taker fee in bps (default: from config.yaml)",
    )
    parser.add_argument(
        "--fee-maker-bps", type=float, default=None,
        help="round-trip maker fee in bps (default: from config.yaml)",
    )
    parser.add_argument(
        "--slippage-bps", type=float, default=None,
        help="one-way slippage assumption in bps (default: from config.yaml)",
    )
    args = parser.parse_args()

    # Costs come from the live config so calibration can never silently
    # diverge from what the bot actually charges. CLI flags allow
    # hypothetical fee schedules ("what fee would make this viable?").
    cfg = load_config(_REPO_ROOT / "config.yaml")
    fee_taker_bps = (
        args.fee_taker_bps
        if args.fee_taker_bps is not None
        else cfg.edge.default_fee_taker * 2 * 1e4
    )
    fee_maker_bps = (
        args.fee_maker_bps
        if args.fee_maker_bps is not None
        else cfg.edge.default_fee_maker * 2 * 1e4
    )
    slippage_bps = (
        args.slippage_bps
        if args.slippage_bps is not None
        else cfg.execution.edge_exit_slippage * 1e4
    )

    rows, skipped_files, skipped_rows = load_rows(args.pattern)
    if not rows:
        print("No usable signal rows found.", file=sys.stderr)
        return 1
    rows.sort(key=lambda r: (r["file"], r["ts"]))

    # Keep files separate so forward moves never cross run boundaries.
    files: list[list[dict]] = []
    current: list[dict] = []
    current_file = None
    for r in rows:
        if r["file"] != current_file:
            if current:
                files.append(current)
            current, current_file = [], r["file"]
        current.append(r)
    if current:
        files.append(current)

    n_total = len(rows)
    n_long = sum(1 for r in rows if r["score"] > 0)
    n_persist = sum(1 for r in rows if r["persistent"])
    print(f"rows={n_total} (valid features) | score>0 (long side): {n_long} | "
          f"persistent=True: {n_persist} | files={len(files)}")
    if skipped_files or skipped_rows:
        print(f"skipped: {skipped_files} file(s) without required columns, "
              f"{skipped_rows} malformed/in-position row(s)")
    print(f"cost model (from config.yaml): taker={fee_taker_bps + slippage_bps:.0f} bps "
          f"+ spread | maker={fee_maker_bps + slippage_bps:.0f} bps")
    print("NOTE: rows are ~1.7s apart and autocorrelated; 'episodes' counts "
          "contiguous groups (gap>15s starts a new one) as a lower bound on "
          "independent samples.\n")

    # (bucket_index, horizon) -> list[(fwd_bps, spread_bps, persistent, episode)]
    cells: dict[tuple[int, int], list[tuple[float, float, bool, str]]] = {}
    n_neg_rows = 0
    for frows in files:
        mids_ts = [r["ts"] for r in frows]
        assert mids_ts == sorted(mids_ts)
        episode_id, last_ts = 0, None
        ep_of: dict[int, str] = {}
        for i in range(len(frows)):
            if last_ts is None or frows[i]["ts"] - last_ts > 15.0:
                episode_id += 1
            last_ts = frows[i]["ts"]
            ep_of[i] = f"{Path(frows[i]['file']).name}#{episode_id}"

            score = frows[i]["score"]
            # Long-only strategy: calibrate on the positive-score side only.
            if score <= 0:
                n_neg_rows += 1
                continue
            b = next((k for k, (lo, hi) in enumerate(SCORE_BUCKETS) if lo <= score < hi), None)
            if b is None:
                continue
            for h in HORIZONS:
                target = frows[i]["ts"] + h
                j = bisect.bisect_left(mids_ts, target)
                if j >= len(frows):
                    continue
                gap = frows[j]["ts"] - target
                # Tight tolerance so a "30s" return is really ~30s: the old
                # max(8, h*0.3) admitted samples spanning eval gaps/staleness.
                if gap > max(2.0, min(30.0, h * 0.1)):
                    continue
                fwd = (frows[j]["mid"] - frows[i]["mid"]) / frows[i]["mid"] * 1e4
                cells.setdefault((b, h), []).append(
                    (fwd, frows[i]["spread_bps"], frows[i]["persistent"], ep_of[i])
                )
    print(f"(score<=0 rows excluded from tables: {n_neg_rows})")
    print()

    # ---- table 1: mean forward move (bps) by score bucket x horizon ----
    print("Mean forward mid move (bps), |score| buckets x horizon [s]:")
    header = "bucket      " + "".join(f"{h:>7}s" for h in HORIZONS)
    print(header)
    for b, (lo, hi) in enumerate(SCORE_BUCKETS):
        line = f"[{lo:.2f},{hi:.2f})"
        for h in HORIZONS:
            vals = [v[0] for v in cells.get((b, h), [])]
            line += (
                f"{fmt(statistics.mean(vals))}"
                if len(vals) >= DISPLAY_MIN_N
                else "       -"
            )
        print(line)

    # ---- table 2: persistence-only subset (entry-like rows) ----
    print("\nSame, persistent=True only (entry-like rows):")
    print(header)
    for b, (lo, hi) in enumerate(SCORE_BUCKETS):
        line = f"[{lo:.2f},{hi:.2f})"
        for h in HORIZONS:
            vals = [v[0] for v in cells.get((b, h), []) if v[2]]
            line += (
                f"{fmt(statistics.mean(vals))}"
                if len(vals) >= DISPLAY_MIN_N
                else "       -"
            )
        print(line)

    # ---- table 3: net expectancy at the most promising horizons ----
    print("\nNet expectancy (mean fwd - cost), persistent=True, bps:")
    print(f"{'bucket':<12}{'H':>5}{'n':>6}{'epis':>6}{'mean':>9}{'median':>9}{'win%':>7}"
          f"{'sprd':>7}{'net_taker':>11}{'net_maker':>11}")
    best: list[tuple[float, int, int, float, int]] = []  # (net_maker, bucket, h, n, ep)
    for b, (lo, hi) in enumerate(SCORE_BUCKETS):
        for h in HORIZONS:
            vals = [v for v in cells.get((b, h), []) if v[2]]
            if len(vals) < args.min_n:
                continue
            fwds = [v[0] for v in vals]
            episodes = len({v[3] for v in vals})
            spread = statistics.median(v[1] for v in vals)
            mean = statistics.mean(fwds)
            net_taker = mean - (fee_taker_bps + spread + slippage_bps)
            net_maker = mean - (fee_maker_bps + slippage_bps)
            win = sum(1 for x in fwds if x > 0) / len(fwds) * 100
            print(f"[{lo:.2f},{hi:.2f}){h:>5}{len(vals):>6}{episodes:>6}{mean:>9.2f}"
                  f"{statistics.median(fwds):>9.2f}{win:>7.1f}{spread:>7.2f}"
                  f"{net_taker:>11.2f}{net_maker:>11.2f}")
            best.append((net_maker, b, h, len(vals), episodes))

    # ---- empirical coefficient: bps of move per unit score ----
    print("\nEmpirical slope (bps per |score|=1) by horizon, persistent=True:")
    for h in HORIZONS:
        pts = []
        for b, (lo, hi) in enumerate(SCORE_BUCKETS):
            vals = [v[0] for v in cells.get((b, h), []) if v[2]]
            if len(vals) >= args.min_n:
                pts.append(((lo + hi) / 2, statistics.mean(vals)))
        if len(pts) >= 2:
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            mx, my = statistics.mean(xs), statistics.mean(ys)
            denom = sum((x - mx) ** 2 for x in xs)
            slope = sum((x - mx) * (y - my) for x, y in pts) / denom if denom else 0.0
            intercept = my - slope * mx
            print(f"  {h:>4}s: slope={slope:8.2f} bps  intercept={intercept:+7.2f} bps  "
                  f"(buckets used: {len(pts)})")

    print("\nBest (net_maker) cells:")
    for net, b, h, n, ep in sorted(best, reverse=True)[:5]:
        lo, hi = SCORE_BUCKETS[b]
        print(f"  score[{lo:.2f},{hi:.2f}) h={h:>3}s  net_maker={net:+.2f} bps  n={n} episodes={ep}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
