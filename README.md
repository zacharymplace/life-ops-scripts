<h1 align="center">🌱 Life Ops Scripts</h1>

<p align="center">
  <a href="https://github.com/zacharymplace/life-ops-scripts/actions/workflows/deploy.yml">
    <img src="https://github.com/zacharymplace/life-ops-scripts/actions/workflows/deploy.yml/badge.svg?branch=main" alt="Deploy" />
  </a>
  <a href="https://github.com/zacharymplace/life-ops-scripts/actions/workflows/ci.yml">
    <img src="https://github.com/zacharymplace/life-ops-scripts/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI" />
  </a>
  <a href="https://github.com/zacharymplace/life-ops-scripts/actions/workflows/link-check.yml">
    <img src="https://github.com/zacharymplace/life-ops-scripts/actions/workflows/link-check.yml/badge.svg?branch=main" alt="Link Check" />
  </a>
  <a href="https://codecov.io/gh/zacharymplace/life-ops-scripts">
    <img src="https://codecov.io/gh/zacharymplace/life-ops-scripts/branch/main/graph/badge.svg" alt="Coverage" />
  </a>
  <a href="https://github.com/zacharymplace/life-ops-scripts/releases">
    <img src="https://img.shields.io/github/v/release/zacharymplace/life-ops-scripts" alt="Release" />
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.11%20|%203.12-blue.svg" alt="Python" />
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/github/license/zacharymplace/life-ops-scripts" alt="License: MIT" />
  </a>
</p>

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [🔧 Purpose](#-purpose)
- [🚀 Getting Started](#-getting-started)
  - [CSV → Parquet (`csv2pq`)](#csv-%E2%86%92-parquet-csv2pq)
  - [Normalize Tiller CSV (to `date,account,description,category,amount`)](#normalize-tiller-csv-to-dateaccountdescriptioncategoryamount)
  - [Cash Flow Rollup (weekly/monthly)](#cash-flow-rollup-weeklymonthly)
- [📂 Repo Layout](#-repo-layout)
- [🧭 Governance](#%F0%9F%A7%AD-governance)
- [🗺 Roadmap](#%F0%9F%97%BA-roadmap)
- [🤝 Contributing](#-contributing)
- [🚀 Releasing](#-releasing)
  - [Steps](#steps)
- [🔗 Links](#-links)
- [📜 License](#-license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

## 🔧 Purpose

Automations for daily life — budgeting helpers, home integrations, and media utilities.
The goal: reduce friction, save time, and make everyday systems more enjoyable.

---

## 🚀 Getting Started

```
# (Optional) create a virtual environment
python -m venv .venv && source .venv/bin/activate
# Windows: .venv\Scripts\activate

# install dev dependencies
pip install -r requirements-dev.txt
# (optional if you add a runtime requirements.txt later)
# pip install -r requirements.txt
```

### CSV → Parquet (`csv2pq`)

Convert CSV to Parquet with optional schema, Arrow dtypes, compression, and index control.

```
python scripts/csv2pq.py docs/examples/in.csv docs/examples/out.parquet \
  --schema docs/examples/schema.yaml \
  --dtype-backend pyarrow \
  --compression zstd \
  --no-index
```

**Flags**
- `--schema`: YAML map `{column: dtype}`; any key containing “date” is parsed as datetime.
- `--dtype-backend`: `numpy` (default) or `pyarrow` for Arrow dtypes in pandas (pandas ≥ 2.0).
- `--compression`: `snappy` (default), `gzip`, `zstd`, `brotli`, or `none`.
- `--index/--no-index`: include or drop the DataFrame index (default: `--no-index`).

**Samples** live in `docs/examples/`:
- `in.csv`, `schema.yaml` → `out.parquet` (used by CI smoke test)

### Normalize Tiller CSV (to `date,account,description,category,amount`)

```
python scripts/python/finance/normalize_tiller_csv.py \
  --infile data/samples/transactions_sample.csv \
  --outdir out
```

Outputs: `out/tiller_normalized.csv`

### Cash Flow Rollup (weekly/monthly)

```
python scripts/python/finance/cash_flow_rollup.py \
  --infile out/tiller_normalized.csv \
  --date-col date \
  --amount-col amount \
  --opening-cash 100000 \
  --freq monthly \
  --outdir out
```

Outputs: `out/cash_monthly_rollup.csv` (or `cash_weekly_rollup.csv`) with inflow, outflow, net, and cumulative cash.

---

## 📂 Repo Layout

```
├─ README.md
├─ scripts/
│  ├─ csv2pq.py          → CSV → Parquet CLI
│  ├─ generate_examples.py
│  └─ python/            → finance utilities
├─ docs/
│  └─ examples/          → sample CSV/Parquet + schema
├─ data/
│  └─ samples/           → demo input data
├─ tests/                → unit & integration tests
├─ .github/
│  ├─ workflows/         → ci.yml, deploy.yml, link-check.yml
│  ├─ ISSUE_TEMPLATE/
│  └─ PULL_REQUEST_TEMPLATE.md
├─ .gitignore
├─ .gitattributes
├─ LICENSE
└─ CHANGELOG.md
```

---

## 🧭 Governance

- **Owner**: Z$
- **Review Cycle**: Quarterly
- **Version**: see latest → Releases badge above
- **Audit Notes**: Track design decisions in `docs/decisions/`
- **Maintainers Guide**: see `docs/MAINTAINERS.md` (governance, PR, release checklists)

---

## 🗺 Roadmap

- [x] Tag-gated Deploy + Releases (artifacts + notes)
- [x] CI smoke test for `csv2pq` (Ubuntu)
- [ ] Tests for finance utilities
- [ ] Package skeleton (`pyproject.toml`) for future publishing
- [ ] More examples & how-tos

---

## 🤝 Contributing

This is primarily a personal project, but feedback, forks, and PRs are welcome.
See `CONTRIBUTING.md`.

---

## 🚀 Releasing

Tagged releases build and publish automatically.

### Steps

1. Ensure `main` is up to date:
   ```
   git checkout main
   git pull --ff-only
   ```
2. Tag and push:
   ```
   git tag v0.1.5
   git push origin v0.1.5
   ```
3. CI/CD will:
   - Run `deploy.sh` to package artifacts into `out/`
   - Upload `life-ops-scripts-<tag>.zip` + `.sha256` to **Releases**
   - Only create a Release on tag runs (manual “Run workflow” won’t create one)

---

## 🔗 Links

- **Releases:** <https://github.com/zacharymplace/life-ops-scripts/releases>
- **Actions (CI):** <https://github.com/zacharymplace/life-ops-scripts/actions>

---

## 📜 License

This project is licensed under the terms of the [MIT License](LICENSE).

---

© Z$ • Life Ops • Code × Clarity

---

<!-- test PR template -->
