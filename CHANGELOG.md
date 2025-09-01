# Changelog
All notable changes to this project will be documented here.

The format is based on **Keep a Changelog**, and this project adheres to **Semantic Versioning**.

## [Unreleased]
### Breaking Changes
- (placeholder) Describe migrations or incompatible changes

### Added
- (placeholder) `--output-format` for rollup (CSV/JSON)
- (placeholder) `--week-start {monday|sunday}`

### Changed
- (placeholder) Improve logging consistency across scripts

### Fixed
- (placeholder) Edge handling for empty input files

---

## [v0.1.7] - 2025-09-01
### Breaking Changes
- None

### Added
- CI: release-assets workflow confirmed stable, auto-attaches `out/` ZIP + SHA256 on tags

### Fixed
- `pqinfo`: cleaned up stray pandas import and syntax error (`ifif head > 0`)
- Bowtie workflow: resolved merge markers, unified label flags, fixed `if` expression

### Quality
- All tests passing (8/8)
- Pre-commit hooks (Black, Ruff, markdownlint, Doctoc) green
- Release process validated through v0.1.6 with attached artifacts

---

## [v0.1.6] - 2025-08-28
### Breaking Changes
- None

### Added
- Release v0.1.6 published with attached assets
- CI workflow verified: `life-ops-scripts-v0.1.6.zip` + `.sha256` auto-generated

---

## [v0.1.5] - 2025-08-27
### Breaking Changes
- None

### Added
- `csv2pq`: dtype-backend, compression, index flags
- Add pyarrow dependency

### Changed
- Pre-commit + `.editorconfig` housekeeping

---

## [v0.1.4] - 2025-08-27
### Breaking Changes
- None

### Added
- `csv2pq.py` CLI
- `generate_examples.py` and example datasets (`in.csv`, `schema.yaml`)
- Workflows: Link Check, Generate Examples

### Changed
- CI and Deploy pipelines
- `.gitattributes`, `.gitignore`, link-check configuration
- README updates

### Chore
- Pre-commit formatting fixes (ruff, EOF newline, trailing whitespace)

---

## [v0.1.3] - 2025-08-27
### Breaking Changes
- None

### Added
- Add `cash_flow_rollup` edge case tests (weekly W–SUN)
- Add `pytest.ini` for repo-root import discovery

### Fixed
- Clean test imports (Ruff E402-safe); remove `sys.path` hacks

### Changed
- Refresh README TOC via Doctoc

---

## [v0.1.2] - 2025-08-24
### Breaking Changes
- None

### Added
- CI: OS/Python matrix (ubuntu & windows; 3.11 & 3.12)
- Codecov integration + coverage upload

### Changed
- Pre-commit: explicitly configures markdownlint; uses repo config in CI

### Fixed
- markdownlint MD024 false-positives for Keep-a-Changelog (allow different nesting)

---

## [v0.1.1] - 2025-08-24
### Breaking Changes
- None

### Added
- `cash_flow_rollup.py` (weekly/monthly) with sample data and a smoke test
- `docs/MAINTAINERS.md` with PR + release checklists
- `.github/PULL_REQUEST_TEMPLATE.md` PR checklist
- `.github/CODEOWNERS` (auto-assigns @zacharymplace)

### Changed
- README: centered badges, TOC, usage, releasing
- CI split: `ci.yml` (lint+test), `deploy.yml` (tagged release)
- Pre-commit tooling: black, ruff, markdownlint (relaxed), doctoc
- Deploy flow: tag → `deploy.sh` builds `zip` + `sha256` → release assets

### Fixed
- Pandas deprecation: switch monthly Grouper from `M`→`ME`

---

## [v0.1.0] - 2025-08-24
### Breaking Changes
- None

### Added
- Initial repo structure, governance docs (CONTRIBUTING, SECURITY, ADR template)
- Actions templates and basic CI

---

<!-- Links -->
[Unreleased]: https://github.com/zacharymplace/life-ops-scripts/compare/v0.1.7...HEAD
[v0.1.7]: https://github.com/zacharymplace/life-ops-scripts/compare/v0.1.6...v0.1.7
[v0.1.6]: https://github.com/zacharymplace/life-ops-scripts/compare/v0.1.5...v0.1.6
[v0.1.5]: https://github.com/zacharymplace/life-ops-scripts/compare/v0.1.4...v0.1.5
[v0.1.4]: https://github.com/zacharymplace/life-ops-scripts/compare/v0.1.3...v0.1.4
[v0.1.3]: https://github.com/zacharymplace/life-ops-scripts/compare/v0.1.2...v0.1.3
[v0.1.2]: https://github.com/zacharymplace/life-ops-scripts/compare/v0.1.1...v0.1.2
[v0.1.1]: https://github.com/zacharymplace/life-ops-scripts/compare/v0.1.0...v0.1.1
[v0.1.0]: https://github.com/zacharymplace/life-ops-scripts/releases/tag/v0.1.0
