---
name: "🚀 Release Checklist"
about: Steps to complete before cutting a release
title: "Release vX.Y.Z"
labels: release
assignees: zacharymplace
---

## 🚀 Release Checklist

## Pre-Release
- [ ] Update `CHANGELOG.md` with version and date
- [ ] Ensure CI is green on `main`
- [ ] Verify `deploy.sh` packages expected files
- [ ] (Optional) Update README usage if behavior changed

## Tag & Release
- [ ] Create tag: `git tag vX.Y.Z && git push origin vX.Y.Z` (or use GitHub “Draft a new release”)
- [ ] Confirm Actions attached artifacts to the Release
- [ ] Publish Release notes (summarize from CHANGELOG)

## Post-Release
- [ ] Open “Release vX.Y.(Z+1) Checklist”
- [ ] Triage any follow-up issues
- [ ] CHANGELOG updated (if user-visible behavior changed)
