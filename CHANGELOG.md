# Changelog
All notable changes to this project will be documented here.

The format is based on **Keep a Changelog**, and this project adheres to **Semantic Versioning**.

## [Unreleased]
### Added
- (placeholder) `--output-format` for rollup (CSV/JSON)
- (placeholder) `--week-start {monday|sunday}`

### Changed
- (placeholder) Improve logging consistency across scripts

### Fixed
- (placeholder) Edge handling for empty input files

---

## [v0.1.1] - 2025-08-24
### Added
- **cash_flow_rollup.py** (weekly/monthly) with sample data and a smoke test
- **docs/MAINTAINERS.md** with PR + release checklists
- **.github/PULL_REQUEST_TEMPLATE.md** PR checklist
- **.github/CODEOWNERS** (auto-assigns @zacharymplace)

### Changed
- README: centered badges, TOC, usage, releasing
- CI split: `ci.yml` (lint+test), `deploy.yml` (tagged release)
- Pre-commit tooling: black, ruff, markdownlint (relaxed), doctoc
- Deploy flow: tag → `deploy.sh` builds `zip` + `sha256` → release assets

### Fixed
- Pandas deprecation: switch monthly Grouper from `M`→`ME`

---

## [v0.1.0] - 2025-08-24
### Added
- Initial repo structure, governance docs (CONTRIBUTING, SECURITY, ADR template)
- Actions templates and basic CI

---

<!-- Links -->
[Unreleased]: https://github.com/zacharymplace/life-ops-scripts/compare/v0.1.1...HEAD
[v0.1.1]: https://github.com/zacharymplace/life-ops-scripts/compare/v0.1.0...v0.1.1
[v0.1.0]: https://github.com/zacharymplace/life-ops-scripts/releases/tag/v0.1.0
