# tests/test_cash_flow_rollup_edges_extra.py
import pandas as pd
from scripts.python.finance.cash_flow_rollup import rollup, Txn

def test_rollup_empty_transactions():
    """Rollup should return an empty DataFrame when given no transactions."""
    df = rollup([])
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_rollup_zero_amount_and_blank_code():
    """Edge case: blank code or zero amount should not crash."""
    txns = [Txn(date="2025-01-01", code="", amount=0.0)]
    df = rollup(txns)
    assert "code" in df.columns
    assert "total" in df.columns
