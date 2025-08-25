# 🌱 Life Ops Scripts
[![CI](https://github.com/zacharymplace/life-ops-scripts/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/zacharymplace/life-ops-scripts/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%20|%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/github/license/zacharymplace/life-ops-scripts)](LICENSE)

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

---

## 📂 Repo Layout

```
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
- **Version**: v0.1.1
- **Audit Notes**: Track design decisions in `docs/decisions/`

---

## 🗺 Roadmap

- [ ] Define first 2-3 scripts or notebooks (e.g., cash flow, hosting helper)
- [ ] Add data samples + tests for reproducibility
- [ ] Wire CI (ruff + pytest)
- [ ] Draft contribution guidelines
- [ ] Publish first release tag (v0.1.1)

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

## 📜 License

This project is licensed under the terms of the MIT License

---

© Z$ • Life Ops • Code × Clarity

---
