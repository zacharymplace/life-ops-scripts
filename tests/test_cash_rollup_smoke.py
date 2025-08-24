import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "sample" / "Tiller_Transactions.csv"
OUTDIR = ROOT / "out"


def run(cmd: str) -> None:
    # Use shell=True to keep it simple across Windows Git Bash/PowerShell
    subprocess.check_call(cmd, cwd=ROOT, shell=True)


def test_pipeline_smoke():
    OUTDIR.mkdir(exist_ok=True)

    # 1) normalize
    run(
        f'python scripts/python/finance/normalize_tiller_csv.py --infile "{SAMPLE}" --outdir "{OUTDIR}"'
    )
    norm = OUTDIR / "tiller_normalized.csv"
    assert norm.exists(), "normalized CSV not created"

    # 2) weekly rollup
    run(
        f'python scripts/python/finance/cash_flow_rollup.py --infile "{norm}" --opening-cash 100000 --freq weekly --outdir "{OUTDIR}"'
    )
    weekly = OUTDIR / "cash_weekly_rollup.csv"
    assert weekly.exists(), "weekly rollup not created"

    # 3) header check
    with weekly.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
    assert header == ["date", "inflow", "outflow", "net", "cash_position"]
