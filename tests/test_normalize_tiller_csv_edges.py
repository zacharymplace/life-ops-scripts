# tests/test_normalize_tiller_csv_edges.py
import pandas as pd
import pytest
from scripts.python.finance import normalize_tiller_csv as norm


def test_normalize_tiller_handles_missing_columns(tmp_path):
    """Ensure normalize_tiller_csv gracefully handles missing headers."""
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("not,a,valid,header\n1,2,3,4\n")
    df = pd.read_csv(bad_csv)
    # Depending on behavior: should raise or handle gracefully
    with pytest.raises(Exception):
        norm.normalize_tiller(df)
