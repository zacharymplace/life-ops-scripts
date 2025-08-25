#!/usr/bin/env bash
set -euo pipefail

# If we're not on a tag (e.g., PR or push to branch), just no-op safely.
# GITHUB_REF_TYPE/GITHUB_REF_NAME are set by GitHub Actions. Locally, they may be empty.
if [[ "${GITHUB_REF_TYPE:-}" != "tag" && -z "${GITHUB_REF_NAME:-}" ]]; then
  echo "[deploy] Not on a tag; no deployment configured. Skipping."
  exit 0
fi

# Derive version from tag or fallback
VERSION="${GITHUB_REF_NAME:-dev}"
ARTDIR="out"
ARTNAME="life-ops-scripts-${VERSION}"
ZIP="${ARTDIR}/${ARTNAME}.zip"
SHA="${ZIP}.sha256"

echo "[deploy] version: ${VERSION}"

# clean/make out dir
rm -rf "${ARTDIR}"
mkdir -p "${ARTDIR}"

# choose what to package (include only if they exist)
INCLUDES=()
for p in scripts docs requirements-dev.txt README.md LICENSE; do
  [[ -e "$p" ]] && INCLUDES+=("$p")
done

# create zip — fail if nothing to include
if [[ ${#INCLUDES[@]} -eq 0 ]]; then
  echo "[deploy] Nothing to package (no expected paths present)." >&2
  exit 1
fi

zip -r "${ZIP}" "${INCLUDES[@]}" >/dev/null

# checksum
shasum -a 256 "${ZIP}" > "${SHA}"

echo "[deploy] built artifacts:"
ls -lh "${ZIP}" "${SHA}"
