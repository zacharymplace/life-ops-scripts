
<h1 align="center">🌱 Life Ops Scripts</h1>

<p align="center">
  <a href="https://github.com/zacharymplace/life-ops-scripts/actions/workflows/ci.yml">
    <img src="https://github.com/zacharymplace/life-ops-scripts/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI" />
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

```bash
# (Optional) create a virtual environment
python -m venv .venv && source .venv/bin/activate
# Windows: .venv\Scripts\activate

# install dev dependencies
pip install -r requirements-dev.txt
# (optional if you add a runtime requirements.txt later)
# pip install -r requirements.txt
```

### Cash Flow Rollup (weekly/monthly)

```bash
python scripts/python/finance/cash_flow_rollup.py \
  --infile out/tiller_normalized.csv \
  --opening-cash 100000 \
  --freq monthly \
  --outdir out
```

Outputs:

- `out/cas_monthly_rollup.csv` (or `cash_weekly_rollup.csv`) with inflow, outflow, net and cumulative cash.

---

## 📂 Repo Layout

```text
├─ README.md
├─ scripts/
│  ├─ python/        → core Python scripts
│  └─ js/            → JavaScript utilities
├─ data/
│  ├─ samples/       → demo input data
├─ docs/             → notes, guides, ADRs
├─ tests/            → unit & integration tests
├─ .github/
│  ├─ ISSUE_TEMPLATE/
│  └─ PULL_REQUEST_TEMPLATE.md
├─ .gitignore
├─ LICENSE
└─ CHANGELOG.md
```

---

## 🧭 Governance

- **Owner**: Z$
- **Review Cycle**: Quarterly
- **Version**: see latest → Releases badge above
- **Audit Notes**: Track design decisions in `docs/decisions/`
- **Maintainers Guide**: see [docs/MAINTAINERS.md](docs/MAINTAINERS.md) for governance, PR, and release checklists

---

## 🗺 Roadmap

- [ ] Define first 2-3 scripts or notebooks (e.g., cash flow, hosting helper)
- [ ] Add data samples + tests for reproducibility
- [ ] Wire CI (ruff + pytest)
- [ ] Draft contribution guidelines
- [ ] Publish new tagged releases regularly

---

## 🤝 Contributing

This is primarily a personal project, but feedback, forks, and PRs are welcome.
See `CONTRIBUTING.md`.

---

## 🚀 Releasing

Tagged releases are built and published automatically by CI.

### Steps

1. Make sure you’re on `main` and up to date:

   ```bash
   git checkout main
   git pull
   ```

2. Tag and push:

   ```bash
   # bump version
   git tag v0.1.2
   git push origin v0.1.2
   ```

3. CI/CD will
   - Run `deploy.sh` to package `scripts/`, `docs/`, and metadata
   - Upload `life-ops-scripts-<tag>.zip` + `.sha256` to the **Releases** page
   - No-op safely if not on a tag

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
