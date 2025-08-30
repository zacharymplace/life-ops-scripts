"""
script: normalize_tiller_csv.py
purpose: Normalize a Tiller Transactions CSV to a compact schema.

usage:
  python scripts/python/finance/normalize_tiller_csv.py \
    --infile ./sample/Tiller_Transactions.csv --outdir ./out

output schema:
  date,account,description,category,amount

audit:
  owner: Z$ | Life Ops
  version: 0.2.0
  last_updated: 2025-08-24
"""

from __future__ import annotations
import argparse
import csv
import pathlib
from dateutil import parser as dtp


FIELDS = ["date", "account", "description", "category", "amount"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Normalize Tiller CSV to a standard schema."
    )
    p.add_argument("--infile", type=pathlib.Path, required=True)
    p.add_argument("--outdir", type=pathlib.Path, default=pathlib.Path("./out"))
    return p.parse_args()


def coerce_date(val: str | None) -> str | None:
    if not val:
        return None
    try:
        return dtp.parse(val).date().isoformat()
    except Exception:
        return None


def clean_text(s: str | None) -> str | None:
    if s is None:
        return None
    s = s.replace("\u200b", "").strip()
    s = " ".join(s.split())
    return s or None


def main() -> int:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    outpath = args.outdir / "tiller_normalized.csv"

    with (
        args.infile.open("r", newline="", encoding="utf-8") as f_in,
        outpath.open("w", newline="", encoding="utf-8") as f_out,
    ):
        r = csv.DictReader(f_in)
        w = csv.DictWriter(f_out, fieldnames=FIELDS)
        w.writeheader()
        for row in r:
            date = coerce_date(row.get("Date") or row.get("date"))
            account = clean_text(row.get("Account"))
            desc = clean_text(
                row.get("Description")
                or row.get("Description 2")
                or row.get("description")
            )
            cat = clean_text(row.get("Category") or row.get("category"))
            amt_raw = row.get("Amount") or row.get("amount") or "0"
            try:
                amt = float(str(amt_raw).replace(",", ""))
            except Exception:
                amt = 0.0

            if not date:
                continue  # skip rows we can't date
            w.writerow(
                {
                    "date": date,
                    "account": account,
                    "description": desc,
                    "category": cat,
                    "amount": amt,
                }
            )

    print(f"[ok] wrote {outpath}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
