# tests/test_normalize_tiller_main_paths.py
import csv
import sys
from pathlib import Path
import pandas as pd
import pytest

# Import the module under test
from scripts.python.finance import normalize_tiller_csv as norm


def write_rows(path: Path, rows: list[dict[str, str]]):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["Date", "Account", "Description", "Category", "Amount"])
        w.writeheader()
        for r in rows:
            w.writerow(r)


def test_normalize_tiller_main_success_and_amount_fallback(tmp_path, capsys, monkeypatch):
    """
    - Hits the happy path (print + return) → covers end-of-main lines.
    - Includes a non-numeric Amount to drive the except → amt=0.0 (covers 78–79-like path).
    """
    infile = tmp_path / "in.csv"
    outdir = tmp_path / "out"
    rows = [
        {"Date": "2025-01-15", "Account": " Checking  ", "Description": " Grocery\tStore ", "Category": "Food", "Amount": "12.34"},
        {"Date": "2025-01-16", "Account": " CC ", "Description": " Gym", "Category": "Health", "Amount": "not-a-number"},  # triggers except → 0.0
    ]
    write_rows(infile, rows)

    # Run CLI main
    monkeypatch.setenv("PYTHONIOENCODING", "utf-8")
    monkeypatch.setattr(sys, "argv", ["normalize_tiller_csv.py", "--infile", str(infile), "--outdir", str(outdir)])
    rc = norm.main()
    captured = capsys.readouterr()

    # Should print [ok] and write the normalized file
    assert rc == 0
    assert "[ok] wrote" in captured.out
    out_csv = outdir / "tiller_normalized.csv"
    assert out_csv.exists()

    df = pd.read_csv(out_csv)
    # date was parsed, text cleaned, second amount coerced to 0.0
    assert df.loc[0, "amount"] == pytest.approx(12.34)
    assert df.loc[1, "amount"] == pytest.approx(0.0)
    # whitespace cleaned
    assert df.loc[0, "account"] == "Checking"
    assert df.loc[0, "description"] == "Grocery Store"


def test_normalize_tiller_skips_bad_date_row(tmp_path, monkeypatch):
    """
    Drive the `if not date: continue` branch (covers 40–43-like path).
    """
    infile = tmp_path / "in2.csv"
    outdir = tmp_path / "out2"
    rows = [
        {"Date": "not-a-date", "Account": "A", "Description": "x", "Category": "y", "Amount": "1"},
        {"Date": "2025-02-01", "Account": "B", "Description": "ok", "Category": "z", "Amount": "2"},
    ]
    with infile.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["Date", "Account", "Description", "Category", "Amount"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    monkeypatch.setattr(sys, "argv", ["normalize_tiller_csv.py", "--infile", str(infile), "--outdir", str(outdir)])
    rc = norm.main()
    assert rc == 0

    out_csv = outdir / "tiller_normalized.csv"
    assert out_csv.exists()
    df = pd.read_csv(out_csv)
    # First row skipped; only valid-dated row remains
    assert len(df) == 1
    assert df.iloc[0]["date"] == "2025-02-01"
