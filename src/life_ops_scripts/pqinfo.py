# src/life_ops_scripts/pqinfo.py
from __future__ import annotations

import click
import pyarrow.parquet as pq


@click.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False, path_type=str))
@click.option("--head", type=int, default=0, help="Show first N rows (reads data).")
def main(file: str, head: int) -> None:
    """
    Print quick info about a Parquet file: rows, row groups, columns, and schema.
    """
    pf = pq.ParquetFile(file)
    schema = pf.schema_arrow

    print(f"path: {file}")
    print(f"rows: {pf.metadata.num_rows}")
    print(f"row_groups: {pf.metadata.num_row_groups}")
    print(f"columns({schema.num_fields}): {[f.name for f in schema]}")
    print("schema:")
    for f in schema:
        print(f"  - {f.name}: {f.type}")

    if head > 0:
        # Only read data when requested
        table = pq.read_table(file).slice(0, head)
        try:
            import pandas as pd  # noqa: F401

            print("\nhead:")
            print(table.to_pandas().to_string(index=False))
        except Exception:
            print("\nhead (Arrow repr):")
            print(table)


if __name__ == "__main__":
    main()
