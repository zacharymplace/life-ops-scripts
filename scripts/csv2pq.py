#!/usr/bin/env python
import pathlib, click, yaml, pandas as pd

@click.command()
@click.argument("csv_path", type=click.Path(exists=True, dir_okay=False))
@click.argument("parquet_path", type=click.Path(dir_okay=False))
@click.option("--schema", type=click.Path(exists=True, dir_okay=False),
              help="YAML mapping {column: dtype}. Datetime cols parsed automatically.")
@click.option("--encoding", default="utf-8-sig", show_default=True)
def main(csv_path, parquet_path, schema, encoding):
    csv_path = pathlib.Path(csv_path)
    parquet_path = pathlib.Path(parquet_path)

    dtype_map, parse_dates = {}, []
    if schema:
        with open(schema, "r", encoding="utf-8") as f:
            m = yaml.safe_load(f) or {}
        for col, dt in m.items():
            s = str(dt).lower()
            if "datetime" in s or "date" in s:
                parse_dates.append(col)
            else:
                dtype_map[col] = dt

    df = pd.read_csv(csv_path, dtype=dtype_map or None,
                     parse_dates=parse_dates or None, encoding=encoding)
    df.to_parquet(parquet_path, index=False)
    click.echo(f"wrote {parquet_path}")

if __name__ == "__main__":
    main()
