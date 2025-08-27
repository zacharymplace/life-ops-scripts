from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/python/finance/normalize_tiller_csv.py"
SAMPLE = ROOT / "data/samples/transactions_sample.csv"
OUTDIR = ROOT / "out"


def test_normalize_smoke():
    OUTDIR.mkdir(exist_ok=True)
    cmd = f'python "{SCRIPT}" --infile "{SAMPLE}" --outdir "{OUTDIR}"'
    subprocess.check_call(cmd, shell=True, cwd=ROOT)
    assert (OUTDIR / "tiller_normalized.csv").exists()
