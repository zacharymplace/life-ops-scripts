from __future__ import annotations

from pathlib import Path
import json
from typing import Optional, Any

import click
import pyarrow.parquet as pq


def inspect_parquet(path: Path) -> dict[str, Any]:
    """Return basic metadata & schema of a Parquet file (best-effort)."""
    pf = pq.ParquetFile(str(path))
    md = pf.metadata
    schema = pf.schema_arrow

    info: dict[str, Any] = {
        "path": str(path),
        "rows": md.num_rows if md else None,
        "columns": md.num_columns if md else len(schema),
        "row_groups": md.num_row_groups if md else None,
        "created_by": getattr(md, "created_by", None) or None,
        "schema": [{"name": f.name, "type": str(f.type)} for f in schema],
    }

    # Best-effort: record compressions for the first row group
    try:
        if md and md.num_row_groups > 0:
            rg0 = md.row_group(0)
            info["compressions"] = [
                str(rg0.column(i).compression) for i in range(info["columns"])
            ]
    except Exception:
        pass

    return info


def collect_stats(md, schema) -> list[dict[str, Any]]:
    """Aggregate null_count/min/max per column across row groups (if present)."""
    out: list[dict[str, Any]] = []
    try:
        if not md:
            return out
        for i, field in enumerate(schema):
            total_nulls = 0
            mins, maxs = [], []
            have_any = False
            for rg_idx in range(md.num_row_groups):
                col = md.row_group(rg_idx).column(i)
                s = getattr(col, "statistics", None)
                if not s:
                    continue
                have_any = True
                if s.null_count is not None:
                    total_nulls += int(s.null_count)
                has_mm = getattr(s, "has_min_max", None)
                if has_mm is True or (s.min is not None or s.max is not None):
                    if s.min is not None:
                        mins.append(s.min)
                    if s.max is not None:
                        maxs.append(s.max)

            if have_any:
                entry: dict[str, Any] = {"name": field.name, "nulls": total_nulls}
                if mins:
                    try:
                        entry["min"] = min(mins)
                    except TypeError:
                        entry["min"] = min(mins, key=lambda x: str(x))
                if maxs:
                    try:
                        entry["max"] = max(maxs)
                    except TypeError:
                        entry["max"] = max(maxs, key=lambda x: str(x))
                out.append(entry)
    except Exception:
        # Stats are optional; ignore if unavailable
        pass
    return out


@click.command(context_settings={"show_default": True})
@click.argument("path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--json", "as_json", is_flag=True, help="Emit machine-readable JSON.")
@click.option("--summary", is_flag=True, help="Only print counts (rows, columns, row_groups).")
@click.option("--head", type=int, default=0, help="Print first N rows (reads data).")
@click.option("-c", "--columns", help="Comma-separated column subset for --head.")
@click.option("--stats", is_flag=True, help="Show per-column nulls/min/max from metadata (best-effort).")
def main(path: Path, as_json: bool, summary: bool, head: int, columns: Optional[str], stats: bool) -> None:
    """Show quick info about a Parquet file."""
    pf = pq.ParquetFile(str(path))
    md = pf.metadata
    schema = pf.schema_arrow

    info = inspect_parquet(path)
    if stats:
        info["stats"] = collect_stats(md, schema)

    if as_json:
        click.echo(json.dumps(info, indent=2))
        return

    if summary:
        click.echo(f"rows={info['rows']} columns={info['columns']} row_groups={info['row_groups']}")
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
        if stats and info.get("stats"):
            click.echo("Stats (metadata):")
            for s in info["stats"]:
                parts = [f"nulls={s.get('nulls')}"]
                if "min" in s:
                    parts.append(f"min={s['min']}")
                if "max" in s:
                    parts.append(f"max={s['max']}")
                click.echo(f"  - {s['name']}: " + " ".join(parts))

    if head > 0:
        cols = None
        if columns:
            cols = [c.strip() for c in columns.split(",") if c.strip()]
        table = pq.read_table(str(path), columns=cols)
        try:
            import pandas as pd  # pandas is already a dependency
            df = table.to_pandas().head(head)
            click.echo()
            click.echo(df.to_string(index=False))
        except Exception:
            click.echo()
            click.echo(str(table.slice(0, head)))


if __name__ == "__main__":
    main()
