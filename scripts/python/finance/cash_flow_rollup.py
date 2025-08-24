"""
script: cash_flow_rollup.py
purpose: Aggregate daily inflows/outflows and compute running cash position.

usage:
  python scripts/python/finance/cash_flow_rollup.py \
    --infile ./out/tiller_normalized.csv \
    --opening-cash 125000 \
    --outdir ./out

inputs:
  --infile        normalized CSV with columns [date, account, description, category, amount]
  --opening-cash  starting balance for running position
  --outdir        where to write rollups

outputs:
  out/cash_daily_rollup.csv  (date, inflow, outflow, net, cash_position)

audit:
  owner: Z$ | Life Ops
  version: 0.1.0
  last_updated: 2025-08-24
"""

from __future__ import annotations
import argparse
import pathlib
import pandas as pd


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Compute daily cash rollup from normalized transactions CSV."
    )
    p.add_argument("--infile", type=pathlib.Path, required=True)
    p.add_argument("--opening-cash", type=float, required=True)
    p.add_argument("--outdir", type=pathlib.Path, default=pathlib.Path("./out"))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.infile)
    # Types
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df = df.dropna(subset=["date"]).copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)

    # Group & roll
    g = df.groupby("date", sort=True)["amount"].sum()
    daily = g.rename("net").reset_index()
    daily["inflow"] = daily["net"].where(daily["net"] > 0, 0.0)
    daily["outflow"] = daily["net"].where(daily["net"] < 0, 0.0).abs()
    daily["cash_position"] = args.opening_cash + daily["net"].cumsum()
    daily = daily[["date", "inflow", "outflow", "net", "cash_position"]]

    outpath = args.outdir / "cash_daily_rollup.csv"
    daily.to_csv(outpath, index=False)
    print(f"[ok] wrote {outpath}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
