# stdlib
import csv
from pathlib import Path  # delete this line if not used later

# third-party
import pandas as pd
import pytest

# local
from scripts.python.finance.cash_flow_rollup import (
    rollup,
    read_transactions,
    setup_log,
)


# ---------- helpers ----------
def _df(rows):
    """rows: list of [txn_date, amount] (strings, numbers)."""
    df = pd.DataFrame(rows, columns=["txn_date", "amount"])
    df["txn_date"] = pd.to_datetime(df["txn_date"], errors="coerce")
    return df


def _write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["txn_date", "amount"])
        w.writerows(rows)


# ---------- unit-ish tests on rollup() ----------
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


def test_bad_dates_are_dropped_and_not_counted():
    df = _df(
        [
            ["not-a-date", 999],  # invalid; should drop
            ["2025-03-02", 100],
            ["2025-03-03", -40],
        ]
    )
    # manually drop invalid here (mimic read_transactions behavior)
    df = df[df["txn_date"].notna()].copy()
    out = rollup(df, "monthly", "txn_date", "amount", opening_cash=500)
    assert len(out) == 1
    row = out.iloc[0]
    assert row["net"] == 60  # 100 - 40
    assert row["cumulative_cash"] == 560


def test_cumulative_cash_is_opening_plus_cumsum():
    df = _df(
        [
            ["2025-04-01", 100],
            ["2025-04-15", -30],
            ["2025-05-01", 10],
        ]
    )
    out_m = rollup(df, "monthly", "txn_date", "amount", opening_cash=1000)
    # first month net = 70, second = 10
    assert list(out_m["net"]) == [70, 10]
    assert list(out_m["cumulative_cash"]) == [1070, 1080]


def test_weekly_groups_multiple_weeks():
    df = _df(
        [
            ["2025-05-05", 100],  # week 1 (Mon)
            ["2025-05-07", -20],  # week 1
            ["2025-05-12", 10],  # week 2
        ]
    )
    out_w = rollup(df, "weekly", "txn_date", "amount", opening_cash=0)
    assert len(out_w) == 2
    # ensure chronological order and expected nets
    assert list(out_w["net"]) == [80, 10]
    assert list(out_w["cumulative_cash"]) == [80, 90]


# ---------- integration-ish test on read_transactions() ----------
def test_empty_csv_exits(tmp_path: Path):
    # create an empty-but-with-header CSV -> should SystemExit in read_transactions
    p = tmp_path / "empty.csv"
    _write_csv(p, [])  # header only
    log = setup_log("ERROR")
    with pytest.raises(SystemExit):
        _ = read_transactions(p, date_col="txn_date", amount_col="amount", log=log)
