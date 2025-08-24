# life-ops-scripts

**Purpose**: Automations for daily life: budgeting helpers, home integrations, media utilities.

## Getting Started
```bash
# Optional: create a virtual environment
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Repo Layout
```
life-ops-scripts/
├─ README.md
├─ scripts/
│  ├─ python/
│  └─ js/
├─ data/
│  ├─ samples/
├─ docs/
├─ tests/
├─ .github/
│  ├─ ISSUE_TEMPLATE/
│  └─ PULL_REQUEST_TEMPLATE.md
├─ .gitignore
├─ LICENSE
└─ CHANGELOG.md
```

## Governance
- Owner: Z$
- Review Cycle: Quarterly
- Version: v0.1.0
- Audit Notes: Track design decisions in `docs/decisions/` (ADR format).

## Roadmap
- [ ] Define first 2–3 scripts or notebooks
- [ ] Add data samples and tests
- [ ] Wire CI (ruff/black or flake8 + pytest)

