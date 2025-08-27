import csv
from pathlib import Path
import sys
import pandas as pd

# Ensure the repo root is importable in CI
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import the module as a whole so we can call its functions
from scripts.python.finance import normalize_tiller_csv as m

def _write_csv(path: Path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

def test_coerce_date_good_and_bad():
    assert m.coerce_date("2025-01-02") == "2025-01-02"
    assert m.coerce_date("Jan 2 2025") == "2025-01-02"
    assert m.coerce_date("not-a-date") is None
    assert m.coerce_date(None) is None

def test_clean_text_trims_and_collapses():
    assert m.clean_text("  A   B  ") == "A B"
    assert m.clean_text("\u200bHidden") == "Hidden"
    assert m.clean_text("   ") is None
    assert m.clean_text(None) is None

def test_normalize_variant_headers(tmp_path: Path):
    # Use "Date / Amount / Description" like raw exports
    p = tmp_path / "raw.csv"
    _write_csv(
        p,
        ["Date", "Account", "Description", "Category", "Amount"],
        [
            ["2025-01-01", "Checking", "Employer", "Income", "2,000.00"],
            ["bad-date", "Checking", "Shop", "Groceries", "100"],  # dropped
            ["2025-01-05", "Checking", "Tacos", "Restaurants", "-150"],
        ],
    )
    # Run the script main() in-process to exercise writer/headers
    outdir = tmp_path / "out"; outdir.mkdir()
    sys.argv = ["normalize_tiller_csv.py", "--infile", str(p), "--outdir", str(outdir)]
    assert m.main() == 0

    out = outdir / "tiller_normalized.csv"
    assert out.exists()
    df = pd.read_csv(out)

    # Your script’s schema
    assert list(df.columns) == list(m.FIELDS)  # ["date","account","description","category","amount"]
    assert len(df) == 2                      # bad-date row dropped
    assert df.loc[0, "date"] == "2025-01-01"
    assert float(df.loc[0, "amount"]) == 2000.0
    assert float(df.loc[1, "amount"]) == -150.0
