# 🌱 Life Ops Scripts 
[![lint](https://github.com/zacharymplace/life-ops-scripts/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/zacharymplace/life-ops-scripts/actions/workflows/lint.yml)
[![python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![license](https://img.shields.io/github/license/zacharymplace/life-ops-scripts)](LICENSE)

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

# install dependencies
pip install -r requirements.txt
```

---

## 📂 Repo Layout

```life-ops-scripts/
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
- **Version**: v0.1.0
- **Audit Notes**: Track design decisions in `docs/decisions/`

---

## 🗺 Roadmap

- [ ] Define first 2-3 scripts or notebooks (e.g., cash flow, hosting helper)
- [ ] Add data smaples + tests for reproducibility
- [ ] Wire CI (ruff + pytest)
- [ ] Draft contribution guidelines
- [ ] Publish first release tag (v0.1.0)

---

## 🤝 Contributing

This is primarily a personal project, but feedback, forks, and PRs are welcome.
See `CONTRIBUTING.md`.

---

## 📜 License

This project is licensed under the terms of the MIT License

---

© Z$ • Life Ops • Code × Clarity

---
