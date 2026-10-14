"""Simulate maker (resting limit) fills on recorded book/matches data.

Answers: would joining the best bid (entry) and joining the best ask
(exit) have filled, and what is the net expectancy per round trip after
maker fees — including adverse selection (fills happen when price trades
to us)?

Run:  python scripts/simulate_maker.py [--run-dir data/raw] [--gate 0.15]
"""
from __future__ import annotations

import argparse
import bisect
import csv
import gzip
import json
import statistics
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from tradebot.config import load_config  # noqa: E402

HORIZONS = (300, 600, 900)


def _open(path: Path):
    return gzip.open(path, "rt") if str(path).endswith(".gz") else path.open()


def load_run(run_dir: Path) -> tuple[list[dict], list[tuple[float, float, float, str]], list[tuple[float, float, float, str, str]]]:
    signals: list[dict] = []
    for sig_path in sorted(run_dir.glob("signals*.csv")):
        with sig_path.open(newline="") as fh:
            for row in csv.DictReader(fh):
                try:
                    signals.append({
                        "ts": float(row["ts"]),
                        "score": float(row["score"]),
                        "mid": float(row["mid"]),
                        "spread_bps": float(row["spread_pct"] or 0.0) * 1e4,
                        "persistent": row["persistent"] == "True",
                    })
                except (TypeError, ValueError, KeyError):
                    continue
    signals.sort(key=lambda r: r["ts"])

    books: list[tuple[float, float, float, str]] = []
    for book_path in sorted(run_dir.glob("books*.jsonl*")):
        with _open(book_path) as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                    books.append((float(obj["ts"]), float(obj["bids"][0][0]), float(obj["asks"][0][0]), obj.get("symbol", "")))
                except (json.JSONDecodeError, KeyError, IndexError, TypeError, ValueError):
                    continue
    books.sort(key=lambda b: b[0])

    seen: set[str] = set()
    matches: list[tuple[float, float, float, str, str]] = []
    for m_path in sorted(run_dir.glob("matches*.jsonl*")):
        with _open(m_path) as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                for m in obj.get("matches", []):
                    mid = m.get("id")
                    if mid in seen:
                        continue
                    seen.add(mid)
                    try:
                        matches.append((float(m["time"]), float(m["price"]), float(m["base_amount"]), m.get("side", ""), obj.get("symbol", "")))
                    except (TypeError, ValueError, KeyError):
                        continue
    matches.sort(key=lambda m: m[0])
    return signals, books, matches


def nearest_book(books: list[tuple[float, float, float, str]], ts: float, tol: float = 3.0) -> tuple[float, float, float, str] | None:
    bts = [b[0] for b in books]
    i = bisect.bisect_left(bts, ts)
    best = None
    for j in (i - 1, i):
        if 0 <= j < len(books) and abs(books[j][0] - ts) <= tol:
            if best is None or abs(books[j][0] - ts) < abs(best[0] - ts):
                best = books[j]
    return best


def simulate_limit_fill(
    side: str,
    price: float,
    size: float,
    t0: float,
    t1: float,
    matches: list[tuple[float, float, float, str, str]],
    mtimes: list[float],
    books: list[tuple[float, float, float, str]],
    bts: list[float],
    at_price_share: float,
) -> tuple[float, float] | None:
    """Return (filled_size, fill_time) or None. Conservative queue model."""
    remaining = size
    fill_time = t1
    lo = bisect.bisect_left(mtimes, t0)
    hi = bisect.bisect_right(mtimes, t1)
    for m_ts, m_px, m_vol, _side, _sym in matches[lo:hi]:
        through = m_px < price if side == "buy" else m_px > price
        at_price = m_px == price
        if through:
            take = min(remaining, m_vol)
        elif at_price and at_price_share > 0:
            take = min(remaining, m_vol * at_price_share)
        else:
            continue
        if take > 0:
            remaining -= take
            fill_time = m_ts
            if remaining <= 1e-9:
                return size, fill_time
    lo_b = bisect.bisect_left(bts, t0)
    hi_b = bisect.bisect_right(bts, t1)
    for b_ts, bid, ask, _sym in books[lo_b:hi_b]:
        crossed = bid < price if side == "buy" else ask > price
        if crossed:
            return size, b_ts
    return None


def run_one_dir(
    run_dir: Path,
    gate: float,
    entry_lifetime: float,
    exit_lifetime: float,
    fee_maker_side_bps: float,
    fee_taker_side_bps: float,
    join_offset_bps: float,
    horizons: list[int],
) -> None:
    signals, books, matches = load_run(run_dir)
    if not signals or not books:
        print(f"{run_dir}: no usable data")
        return
    from collections import Counter

    sym_counts = Counter(b[3] for b in books if b[3])
    if sym_counts:
        target = sym_counts.most_common(1)[0][0]
        books = [b for b in books if b[3] == target]
        matches = [m for m in matches if m[4] == target]
        other = {s: n for s, n in sym_counts.items() if s != target}
        print(f"symbol={target} (filtered out: {other or 'none'})")
    bts = [b[0] for b in books]
    mtimes = [m[0] for m in matches]
    span = signals[-1]["ts"] - signals[0]["ts"]
    print(f"\n=== {run_dir} ===")
    print(f"signals={len(signals)} span={span/60:.0f}min books={len(books)} "
          f"({(books[-1][0]-books[0][0])/max(1,len(books)-1):.2f}s cadence) "
          f"matches={len(matches)}")
    cands = [r for r in signals if r["persistent"] and r["score"] >= gate]
    print(f"entry candidates (persistent, score>={gate}): {len(cands)}")
    if not cands:
        return

    implied_size = 950_000.0 / cands[0]["mid"]
    print(f"implied position size: {implied_size:.2f} base units")

    for h in horizons:
        rows = []
        for r in cands:
            snap = nearest_book(books, r["ts"])
            if snap is None:
                continue
            _btsig, bid, ask, _sym = snap
            snap_mid = (bid + ask) / 2
            if r["mid"] > 0 and abs(snap_mid / r["mid"] - 1) > 0.02:
                continue  # incompatible archive (different regime/unit): skip
            entry_px = bid * (1 - join_offset_bps / 1e4)
            t1 = r["ts"] + entry_lifetime
            fill = None
            for share in (0.0, 1.0):
                fill = simulate_limit_fill(
                    "buy", entry_px, implied_size, r["ts"], t1, matches, mtimes, books, bts, share
                )
                if fill:
                    break
            t_exit = r["ts"] + h
            exit_snap = nearest_book(books, t_exit, tol=10.0)
            if exit_snap is None:
                continue
            if abs((exit_snap[1] + exit_snap[2]) / 2 / snap_mid - 1) > 0.05:
                continue  # exit book from another regime: skip
            if fill is None:
                fwd = (exit_snap[2] + exit_snap[1]) / 2 / r["mid"] - 1
                rows.append({"filled": False, "fwd_bps": fwd * 1e4})
                continue
            filled_size, _ = fill
            exit_ask = exit_snap[2]
            exit = None
            for share in (0.0, 1.0):
                exit = simulate_limit_fill(
                    "sell", exit_ask, filled_size, t_exit, t_exit + exit_lifetime,
                    matches, mtimes, books, bts, share,
                )
                if exit:
                    break
            if exit:
                sell_px = exit_ask
                exit_fee = fee_maker_side_bps
                exit_kind = "maker"
            else:
                last = nearest_book(books, t_exit + exit_lifetime, tol=30.0)
                sell_px = last[1] if last else exit_snap[1]
                exit_fee = fee_taker_side_bps
                exit_kind = "taker"
            net = (sell_px - entry_px) / entry_px * 1e4 - fee_maker_side_bps - exit_fee
            rows.append({
                "filled": True,
                "net_bps": net,
                "exit_kind": exit_kind,
                "adverse_bps": (entry_px - r["mid"]) / r["mid"] * 1e4,
                "fwd_bps": (exit_snap[2] + exit_snap[1]) / 2 / r["mid"] - 1e4 / 1e4,
            })
        if not rows:
            continue
        filled = [x for x in rows if x["filled"]]
        n = len(rows)
        fill_pct = len(filled) / n * 100
        n_maker_ex = sum(1 for x in filled if x["exit_kind"] == "maker")
        n_tk = len(filled) - n_maker_ex
        cond_mean = statistics.mean(x["net_bps"] for x in filled) if filled else float("nan")
        per_signal = cond_mean * len(filled) / n if filled else 0.0
        taker_ref = statistics.mean(
            x["fwd_bps"] - fee_taker_side_bps * 2 - x.get("spread_bps", 16.0) - 5.0 for x in rows
        ) if rows else float("nan")
        med = statistics.median(x["net_bps"] for x in filled) if filled else float("nan")
        win = sum(1 for x in filled if x["net_bps"] > 0) / len(filled) * 100 if filled else 0.0
        adverse = statistics.mean(x["adverse_bps"] for x in filled) if filled else float("nan")
        print(f"\nH={h}s  signals={n}")
        print(f"  entry fills: {len(filled)} ({fill_pct:.0f}%)  "
              f"maker exits: {n_maker_ex}  taker flatten: {n_tk}")
        print(f"  adverse selection at fill: {adverse:+.1f} bps vs signal mid")
        print(f"  net per filled trade: mean={cond_mean:+.1f}  median={med:+.1f}  win%={win:.0f}")
        print(f"  net per signal (unfilled=0): {per_signal:+.1f} bps")
        print(f"  taker reference on same signals: {taker_ref:+.1f} bps")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", action="append", default=None)
    parser.add_argument("--gate", type=float, default=0.15)
    parser.add_argument("--entry-lifetime", type=float, default=60.0)
    parser.add_argument("--exit-lifetime", type=float, default=30.0)
    parser.add_argument("--join-offset-bps", type=float, default=0.0)
    parser.add_argument("--fee-maker-bps", type=float, default=None)
    parser.add_argument("--fee-taker-bps", type=float, default=None)
    parser.add_argument(
        "--horizons",
        default="300,600,900",
        help="comma-separated hold horizons in seconds, e.g. 300,1800,3600,7200",
    )
    args = parser.parse_args()
    horizons = [int(x) for x in args.horizons.split(",") if x.strip()]
    cfg = load_config(_REPO_ROOT / "config.yaml")
    fee_maker = args.fee_maker_bps if args.fee_maker_bps is not None else cfg.edge.default_fee_maker * 1e4
    fee_taker = args.fee_taker_bps if args.fee_taker_bps is not None else cfg.edge.default_fee_taker * 1e4
    dirs = args.run_dir or ["data/raw", "data/calib"]
    for d in dirs:
        p = Path(d) if Path(d).is_absolute() else _REPO_ROOT / d
        if not (p / "books.jsonl").exists():
            print(f"skip {p} (no books.jsonl)")
            continue
        run_one_dir(p, args.gate, args.entry_lifetime, args.exit_lifetime, fee_maker, fee_taker, args.join_offset_bps, horizons)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
