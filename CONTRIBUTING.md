# 🤝 Contributing Guide

Thanks for checking out **Life Ops Scripts**!
This is primarily a personal project, but contributions, suggestions, and forks are welcome.

---

## 🔄 Workflow

- Branch from `dev` (e.g., `feat/short-description`).
- Open a Pull Request targeting `dev`.
- Squash + merge once approved.
- Periodically promote `dev` → `main` with a version bump.

---

## 📌 Standards

- Add or update **README sections** when you change behavior.
- Place tests in `tests/` — even lightweight coverage is better than none.
- Keep scripts **idempotent and safe** (dry-run flags, backups).
- Follow existing folder structure (`scripts/`, `docs/`, `tests/`).

---

## 🧹 Code Style

- **Python 3.11+**
- Lint/format with [ruff](https://docs.astral.sh/ruff/) + [black](https://black.readthedocs.io/en/stable/).
- Commit messages: short + imperative (e.g., `feat: add cash flow summary script`).
- Branch naming: `feat/`, `fix/`, `chore/`.

---

## 🚀 Release

- **Semantic versioning**: `MAJOR.MINOR.PATCH`
- Update **CHANGELOG.md** with notable changes.
- Tag releases from `main` once promoted.

---

## 📜 Notes

- This repo evolves organically — not every idea will be merged, but discussion is welcome.
- For big ideas, open an **issue** first to align.

---

© Z$ • Life Ops • Code × Clarity
