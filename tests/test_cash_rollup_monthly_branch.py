import pandas as pd
from scripts.python.finance.cash_flow_rollup import rollup


def test_rollup_monthly_branch():
    df = pd.DataFrame(
        {
            "txn_date": pd.to_datetime(["2025-01-10", "2025-01-31", "2025-02-01"]),
            "amount": [100.0, -40.0, 25.0],
        }
    )
    out = rollup(
        df,
        freq="monthly",
        date_col="txn_date",
        amount_col="amount",
        opening_cash=1000.0,
    )

    assert list(out["label"]) == ["2025-01", "2025-02"]

    jan = out.iloc[0]
    feb = out.iloc[1]
    # inflow/outflow are derived from NET, not individual positives/negatives
    assert jan["net"] == 60.0 and jan["inflow"] == 60.0 and jan["outflow"] == 0.0
    assert feb["net"] == 25.0 and feb["inflow"] == 25.0 and feb["outflow"] == 0.0
    assert feb["cumulative_cash"] == 1000.0 + 60.0 + 25.0
