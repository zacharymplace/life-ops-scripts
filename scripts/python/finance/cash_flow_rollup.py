"""
script: cash_flow_rollup.py
purpose: Aggregate inflows/outflows and compute running cash position
         at daily, weekly, or monthly frequency.

usage:
  python scripts/python/finance/cash_flow_rollup.py \
    --infile ./out/tiller_normalized.csv \
    --opening-cash 125000 \
    --freq weekly \
    --outdir ./out

audit:
  owner: Z$ | Life Ops
  version: 0.3.0
  last_updated: 2025-08-24
"""

from __future__ import annotations
import argparse
import pathlib
import pandas as pd


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Compute cash rollup from normalized transactions CSV."
    )
    p.add_argument("--infile", type=pathlib.Path, required=True)
    p.add_argument("--opening-cash", type=float, required=True)
    p.add_argument("--freq", choices=["daily", "weekly", "monthly"], default="daily")
    p.add_argument("--outdir", type=pathlib.Path, default=pathlib.Path("./out"))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.infile)

    # Required columns guard
    required = {"date", "amount"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"[error] missing required columns: {sorted(missing)}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)

    if args.freq == "daily":
        g = df.groupby(df["date"].dt.date)["amount"].sum()
    elif args.freq == "weekly":
        g = df.groupby(pd.Grouper(key="date", freq="W-MON"))["amount"].sum()
    elif args.freq == "monthly":
        g = df.groupby(pd.Grouper(key="date", freq="ME"))["amount"].sum()

    roll = g.rename("net").reset_index()
    roll["inflow"] = roll["net"].where(roll["net"] > 0, 0.0)
    roll["outflow"] = roll["net"].where(roll["net"] < 0, 0.0).abs()
    roll["cash_position"] = args.opening_cash + roll["net"].cumsum()
    roll = roll[["date", "inflow", "outflow", "net", "cash_position"]]

    outpath = args.outdir / f"cash_{args.freq}_rollup.csv"
    roll.to_csv(outpath, index=False)
    print(f"[ok] wrote {outpath}")
    print(
        f"[ok] rows={len(roll)} | inflow={roll['inflow'].sum():.2f} "
        f"| outflow={roll['outflow'].sum():.2f} | cash_end={roll['cash_position'].iloc[-1]:.2f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
