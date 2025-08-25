#!/usr/bin/env bash
set -euo pipefail

# Derive version from tag or fallback (runner sets GITHUB_REF_NAME on tags)
VERSION="${GITHUB_REF_NAME:-dev}"
ARTDIR="out"
ARTNAME="life-ops-scripts-${VERSION}"
ZIP="${ARTDIR}/${ARTNAME}.zip"
SHA="${ZIP}.sha256"

echo "[deploy] version: ${VERSION}"

# clean/make out dir
rm -rf "${ARTDIR}"
mkdir -p "${ARTDIR}"

# choose what to package
INCLUDES=(
  "scripts"
  "docs"
  "requirements-dev.txt"
  "README.md"
  "LICENSE"
)

# create zip (only include paths that exist)
zip -r "${ZIP}" "${INCLUDES[@]}" 2>/dev/null || true

# ensure we packed something
if [[ ! -s "${ZIP}" ]]; then
  echo "[deploy] Nothing to package. Did you remove the expected paths?" >&2
  exit 1
fi

# checksum
shasum -a 256 "${ZIP}" > "${SHA}"

echo "[deploy] built:"
ls -lh "${ZIP}" "${SHA}"
