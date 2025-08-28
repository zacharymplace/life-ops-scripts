#!/usr/bin/env python
from __future__ import annotations

import pathlib
from typing import Dict, List

import click
import pandas as pd
import yaml


def _load_schema(schema_path: pathlib.Path) -> tuple[Dict[str, str], List[str]]:
    """Return (dtype_map, parse_dates) from a YAML {column: dtype} file."""
    if not schema_path:
        return {}, []
    with open(schema_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    dtype_map: Dict[str, str] = {}
    parse_dates: List[str] = []
    for col, dt in raw.items():
        s = str(dt).lower()
        if "date" in s:  # treat any *date*/*datetime* as parsed date
            parse_dates.append(col)
        else:
            dtype_map[col] = str(dt)
    return dtype_map, parse_dates


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument(
    "csv_path", type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path)
)
@click.argument("parquet_path", type=click.Path(dir_okay=False, path_type=pathlib.Path))
@click.option(
    "--schema",
    type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path),
    help="YAML mapping {column: dtype}. Datetime-like cols auto-parsed.",
)
@click.option(
    "--dtype-backend",
    type=click.Choice(["numpy", "pyarrow"], case_sensitive=False),
    default="numpy",
    show_default=True,
    help="Use Arrow dtypes end-to-end with 'pyarrow' (pandas>=2.0).",
)
@click.option(
    "--compression",
    type=click.Choice(
        ["snappy", "gzip", "zstd", "brotli", "none"], case_sensitive=False
    ),
    default="snappy",
    show_default=True,
    help="Parquet compression codec.",
)
@click.option(
    "--encoding", default="utf-8-sig", show_default=True, help="CSV text encoding."
)
@click.option(
    "--index/--no-index",
    default=False,
    show_default=True,
    help="Write DataFrame index.",
)
def main(
    csv_path: pathlib.Path,
    parquet_path: pathlib.Path,
    schema: pathlib.Path | None,
    dtype_backend: str,
    compression: str,
    encoding: str,
    index: bool,
) -> None:
    """Convert CSV → Parquet with optional schema + Arrow dtype backend."""
    dtype_map, parse_dates = _load_schema(schema) if schema else ({}, [])

    # pandas.read_csv supports dtype_backend=['numpy_nullable','pyarrow'] (pandas >=2.0)
    dtype_backend_val = (
        "numpy_nullable" if dtype_backend.lower() == "numpy" else "pyarrow"
    )

    read_csv_kwargs = dict(
        dtype=(dtype_map or None),
        parse_dates=(parse_dates or None),
        encoding=encoding,
    )
    # Pass dtype_backend if this pandas supports it
    try:
        df = pd.read_csv(csv_path, dtype_backend=dtype_backend_val, **read_csv_kwargs)  # type: ignore[arg-type]
    except TypeError:
        # Older pandas: fall back without dtype_backend
        df = pd.read_csv(csv_path, **read_csv_kwargs)

    comp = None if compression.lower() == "none" else compression.lower()
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(parquet_path, index=index, compression=comp)
    click.echo(f"wrote {parquet_path}  rows={len(df)}  cols={list(df.columns)}")


if __name__ == "__main__":
    main()
