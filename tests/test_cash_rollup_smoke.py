from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/python/finance/cash_flow_rollup.py"
SAMPLE = ROOT / "data/samples/transactions_sample.csv"
OUTDIR = ROOT / "out"


def test_pipeline_runs():
    OUTDIR.mkdir(exist_ok=True)
    cmd = (
        f'python "{SCRIPT}" --infile "{SAMPLE}" '
        f'--opening-cash 100000 --freq monthly --outdir "{OUTDIR}"'
    )
    subprocess.check_call(cmd, shell=True, cwd=ROOT)
    assert (OUTDIR / "cash_monthly_rollup.csv").exists()
