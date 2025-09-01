# tests/test_import_smoke.py

def test_import_life_ops_scripts_smoke():
    """Ensure top-level package can be imported (silences coverage warning)."""
    __import__("life_ops_scripts")
