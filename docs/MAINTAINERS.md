# MAINTAINERS

**Repo:** `life-ops-scripts`
**Owner:** Z$
**Purpose:** Automations for budgeting, home integrations, and media utilities.

---

## Contacts

- **Primary:** Z$ (GitHub: zacharymplace)
- **Security reports:** see [SECURITY.md](../SECURITY.md)

---

## Decision Flow

- Small changes: maintainer discretion, merge when checks pass.
- Larger changes (release process, CI, structure): open an issue → capture decision as an ADR in `docs/decisions/`.

---

## Branch & Merge Policy

- Default branch: main
- All changes via PRs (squash & merge)
- Required checks:
  - CI / lint (ci.yml)
  - CI / test (ci.yml)
- Keep main linear (`git pull --rebase`)

---

## PR Checklist (copy into PR)

- [ ] Targets main
- [ ] Lint passes (black, ruff)
- [ ] Tests present/updated (if logic changed)
- [ ] Docs/README updated (if user-visible change)
- [ ] Safe by default (dry-run/backups where relevant)

Local helpers:
    pre-commit run --all-files
    pytest -q

---

## Release Checklist

Tagged releases build & attach artifacts automatically.

1. Update main:
       git checkout main
       git pull --rebase
2. Tag & push:
       git tag vX.Y.Z
       git push origin vX.Y.Z
3. CI runs deploy.sh → uploads:
   - life-ops-scripts-vX.Y.Z.zip
   - life-ops-scripts-vX.Y.Z.zip.sha256
4. Verify Releases page and note changes in CHANGELOG.md (optional).

Note: a Makefile helper is available — `make release v=X.Y.Z`

---

## Versioning

- Semantic Versioning: MAJOR.MINOR.PATCH
- Breaking changes → bump MAJOR
- New features → MINOR
- Fixes/docs/infra → PATCH

---

## CI/CD Notes

- CI (ci.yml): lint + tests on PRs & pushes
- Deploy (deploy.yml): only on tag push; uses ncipollo/release-action
- Old workflows archived under .github/workflows-archive/

---

## Pre-commit Hooks

Auto-polish:

- black, ruff
- markdownlint (emoji anchors disabled)
- doctoc (updates README TOC)

---

## Labels (suggested)

- feat, fix, docs, chore, infra
- good first issue

---

## Repo Hygiene

- Auto-delete merged branches (enabled)
- Keep ADRs for notable changes in docs/decisions/
