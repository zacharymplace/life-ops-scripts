from __future__ import annotations

from pathlib import Path
import json

import click
import pyarrow.parquet as pq
import pandas as pd


def inspect_parquet(path: Path) -> dict:
    """Return basic metadata & schema of a Parquet file."""
    pf = pq.ParquetFile(str(path))
    md = pf.metadata
    schema = pf.schema_arrow

    info = {
        "path": str(path),
        "rows": md.num_rows,
        "columns": md.num_columns,
        "row_groups": md.num_row_groups,
        "created_by": getattr(md, "created_by", None) or None,
        "schema": [{"name": f.name, "type": str(f.type)} for f in schema],
    }

    # Best-effort: compressions for the first row group (if present)
    try:
        if md.num_row_groups > 0:
            rg0 = md.row_group(0)
            info["compressions"] = [
                str(rg0.column(i).compression) for i in range(md.num_columns)
            ]
    except Exception:
        pass

    return info


@click.command(context_settings={"show_default": True})
@click.argument("path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--json", "as_json", is_flag=True, help="Emit machine-readable JSON.")
@click.option(
    "--summary",
    is_flag=True,
    help="Only print counts (rows, columns, row_groups).",
)
@click.option("--head", type=int, default=0, help="Print first N rows (reads data).")
def main(path: Path, as_json: bool, summary: bool, head: int) -> None:
    """Show quick info about a Parquet file."""
    info = inspect_parquet(path)

    if as_json:
        click.echo(json.dumps(info, indent=2))
        return

    if summary:
        click.echo(
            f"rows={info['rows']} columns={info['columns']} "
            f"row_groups={info['row_groups']}"
        )
    else:
        click.echo(f"File: {info['path']}")
        click.echo(f"Rows: {info['rows']}")
        click.echo(f"Columns: {info['columns']}")
        click.echo(f"Row groups: {info['row_groups']}")
        if info.get("created_by"):
            click.echo(f"Created by: {info['created_by']}")
        click.echo("Schema:")
        for f in info["schema"]:
            click.echo(f"  - {f['name']}: {f['type']}")

    if head > 0:
        df = pd.read_parquet(path, engine="pyarrow")
        click.echo()
        click.echo(df.head(head).to_string(index=False))


if __name__ == "__main__":
    main()
