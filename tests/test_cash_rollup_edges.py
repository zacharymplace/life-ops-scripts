from pathlib import Path
import csv
import pandas as pd
import pytest

from scripts.python.finance.cash_flow_rollup import (
    rollup,
    read_transactions,
    setup_log,
)


def _df(rows):
    """rows: list of [txn_date, amount]."""
    df = pd.DataFrame(rows, columns=["txn_date", "amount"])
    df["txn_date"] = pd.to_datetime(df["txn_date"], errors="coerce")
    return df


def _write_csv(path: Path, rows):
    """Write rows to CSV with header txn_date,amount."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["txn_date", "amount"])
        w.writerows(rows)


def test_only_inflows_monthly():
    df = _df(
        [
            ["2025-01-01", 200],
            ["2025-01-15", 50],
        ]
    )
    out = rollup(
        df, freq="monthly", date_col="txn_date", amount_col="amount", opening_cash=1000
    )
    assert len(out) == 1
    row = out.iloc[0]
    assert row["inflow"] == 250
    assert row["outflow"] == 0
    assert row["net"] == 250
    assert row["cumulative_cash"] == 1250


def test_only_outflows_weekly():
    df = _df(
        [
            ["2025-02-03", -25],  # Mon
            ["2025-02-07", -75],  # Fri
        ]
    )
    out = rollup(
        df, freq="weekly", date_col="txn_date", amount_col="amount", opening_cash=1000
    )
    assert len(out) == 1
    row = out.iloc[0]
    assert row["inflow"] == 0
    assert row["outflow"] == 100
    assert row["net"] == -100
    assert row["cumulative_cash"] == 900


def test_bad_dates_dropped_not_counted():
    df = _df(
        [
            ["not-a-date", 999],  # invalid → dropped
            ["2025-03-02", 100],
            ["2025-03-03", -40],
        ]
    )
    df = df[df["txn_date"].notna()].copy()  # mimic read_transactions behavior
    out = rollup(df, "monthly", "txn_date", "amount", opening_cash=500)
    assert len(out) == 1
    row = out.iloc[0]
    assert row["net"] == 60
    assert row["cumulative_cash"] == 560


def test_weekly_multiple_periods_and_order():
    df = _df(
        [
            ["2025-05-05", 100],  # week 1 (Mon)
            ["2025-05-07", -20],  # week 1
            ["2025-05-12", 10],  # week 2
        ]
    )
    out = rollup(df, "weekly", "txn_date", "amount", opening_cash=0)
    assert len(out) == 2
    # chronological order + correct nets/cumulative
    assert list(out["net"]) == [80, 10]
    assert list(out["cumulative_cash"]) == [80, 90]


def test_cumulative_cash_is_opening_plus_cumsum():
    df = _df(
        [
            ["2025-04-01", 100],
            ["2025-04-15", -30],
            ["2025-05-01", 10],
        ]
    )
    out = rollup(df, "monthly", "txn_date", "amount", opening_cash=1000)
    assert list(out["net"]) == [70, 10]
    assert list(out["cumulative_cash"]) == [1070, 1080]


def test_empty_csv_exits(tmp_path: Path):
    p = tmp_path / "empty.csv"
    _write_csv(p, [])  # header only
    log = setup_log("ERROR")
    with pytest.raises(SystemExit):
        _ = read_transactions(p, date_col="txn_date", amount_col="amount", log=log)


def test_missing_required_columns_exits(tmp_path: Path):
    # no 'amount' column → should exit
    p = tmp_path / "missing.csv"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["txn_date", "category"])
        w.writerow(["2025-01-01", "Other"])
    log = setup_log("ERROR")
    with pytest.raises(SystemExit):
        _ = read_transactions(p, date_col="txn_date", amount_col="amount", log=log)
