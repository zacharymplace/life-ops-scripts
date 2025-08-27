#!/usr/bin/env python
"""
cash_flow_rollup.py

Roll up normalized transactions by week or month, compute net and cumulative cash.

Expected CSV columns:
- txn_date (YYYY-MM-DD)
- amount   (positive=inflow, negative=outflow)
Optional: category, merchant, memo
"""

from __future__ import annotations
import argparse
import logging
from pathlib import Path
import sys
import pandas as pd


def setup_log(level: str = "INFO") -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(levelname)s %(message)s",
    )
    return logging.getLogger("cash_flow_rollup")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Cash flow rollup by week/month.")
    p.add_argument("--infile", required=True, help="Normalized transactions CSV")
    p.add_argument("--outdir", default="out", help="Output directory")
    p.add_argument(
        "--freq",
        choices=("weekly", "monthly"),
        default="monthly",
        help="Rollup frequency",
    )
    p.add_argument(
        "--opening-cash", type=float, required=True, help="Opening cash balance"
    )
    p.add_argument("--date-col", default="txn_date")
    p.add_argument("--amount-col", default="amount")
    p.add_argument("--log-level", default="INFO")
    return p.parse_args()


def read_transactions(
    path: Path, date_col: str, amount_col: str, log: logging.Logger
) -> pd.DataFrame:
    if not path.exists():
        log.error("Input file not found: %s", path)
        sys.exit(1)
    df = pd.read_csv(path)
    if date_col not in df.columns or amount_col not in df.columns:
        log.error("Missing required columns: %s, %s", date_col, amount_col)
        sys.exit(1)
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df[df[date_col].notna()].copy()
    df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")
    df = df[df[amount_col].notna()].copy()
    if df.empty:
        log.error("No valid rows after coercion.")
        sys.exit(1)
    return df.sort_values(date_col)


def rollup(
    df: pd.DataFrame, freq: str, date_col: str, amount_col: str, opening_cash: float
) -> pd.DataFrame:
    if freq == "monthly":
        # Month end grouping
        g = df.groupby(pd.Grouper(key=date_col, freq="ME"))
        out = g[amount_col].sum().reset_index()
        out.rename(columns={amount_col: "net", date_col: "period_end"}, inplace=True)
        out["period_start"] = out["period_end"].dt.to_period("M").dt.start_time
        out["label"] = out["period_start"].dt.to_period("M").astype(str)
    else:
        # Week starts Monday, ends Sunday -> group by weeks ending Sunday
        g = df.groupby(pd.Grouper(key=date_col, freq="W-SUN"))
        out = g[amount_col].sum().reset_index()
        out.rename(columns={amount_col: "net", date_col: "period_end"}, inplace=True)
        out["period_start"] = out["period_end"] - pd.Timedelta(days=6)
        # Human-readable label (week start date)
        out["label"] = out["period_start"].dt.strftime("%Y-%m-%d")

    # chronological order
    out = out.sort_values("period_start").reset_index(drop=True)

    # inflow/outflow split and cumulative cash
    out["inflow"] = out["net"].clip(lower=0)
    out["outflow"] = out["net"].clip(upper=0).abs()
    out["opening_cash"] = opening_cash
    out["cumulative_cash"] = opening_cash + out["net"].cumsum()

    cols = [
        "label",
        "period_start",
        "period_end",
        "inflow",
        "outflow",
        "net",
        "opening_cash",
        "cumulative_cash",
    ]
    return out[cols]


def main() -> None:
    args = parse_args()
    log = setup_log(args.log_level)
    infile = Path(args.infile)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = read_transactions(infile, args.date_col, args.amount_col, log)
    rolled = rollup(df, args.freq, args.date_col, args.amount_col, args.opening_cash)

    outname = f"cash_{args.freq}_rollup.csv"
    outfile = outdir / outname
    rolled.to_csv(outfile, index=False)
    log.info("Wrote %s", outfile)


if __name__ == "__main__":
    main()
