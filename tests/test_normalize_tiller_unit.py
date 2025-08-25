import csv
from pathlib import Path
import pandas as pd
from scripts.python.finance.normalize_tiller_csv import coerce_date, clean_text, FIELDS

def _write_csv(path: Path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

def test_coerce_date_good_and_bad():
    assert coerce_date("2025-01-02") == "2025-01-02"
    assert coerce_date("Jan 2 2025") == "2025-01-02"
    assert coerce_date("not-a-date") is None
    assert coerce_date(None) is None

def test_clean_text_trims_and_collapses():
    assert clean_text("  A   B  ") == "A B"
    assert clean_text("\u200bHidden") == "Hidden"
    assert clean_text("   ") is None
    assert clean_text(None) is None

def test_normalize_variant_headers(tmp_path: Path, monkeypatch):
    # Use variant headers: "Date, Amount, Description" like raw exports
    p = tmp_path / "raw.csv"
    _write_csv(
        p,
        ["Date", "Account", "Description", "Category", "Amount"],
        [
            ["2025-01-01", "Checking", "Employer", "Income", "2,000.00"],
            ["bad-date", "Checking", "Shop", "Groceries", "100"],   # dropped
            ["2025-01-05", "Checking", "Tacos", "Restaurants", "-150"],
        ],
    )

    # Run the module's main() in-process with simulated argv
    from scripts.python.finance import normalize_tiller_csv as m
    outdir = tmp_path / "out"
    outdir.mkdir()
    import sys
    sys.argv = ["normalize_tiller_csv.py", "--infile", str(p), "--outdir", str(outdir)]
    assert m.main() == 0

    out = outdir / "tiller_normalized.csv"
    assert out.exists()
    df = pd.read_csv(out)

    # Expected header from your script
    assert list(df.columns) == FIELDS  # ["date","account","description","category","amount"]

    # Dropped invalid row; 2 valid rows remain in chronological order
    assert len(df) == 2
    assert df.loc[0, "date"] == "2025-01-01"
    assert float(df.loc[0, "amount"]) == 2000.0
    assert float(df.loc[1, "amount"]) == -150.0
