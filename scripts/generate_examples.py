from pathlib import Path
import pandas as pd

out = Path("docs/examples")
out.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame(
    {
        "entity": ["A", "A", "B", "B"],
        "dept": ["Ops", "Ops", "Fin", "Fin"],
        "month": pd.to_datetime(["2025-06-01","2025-07-01","2025-06-01","2025-07-01"]),
        "amount": [1200.25, 1300.75, 900.00, 950.50],
        "flag": [True, False, True, False],
    }
)

df.to_csv(out / "pq_handoff_sample.csv", index=False)
df.to_parquet(out / "pq_handoff_sample.parquet", index=False)
print("Wrote:", list(out.glob("pq_handoff_sample.*")))
