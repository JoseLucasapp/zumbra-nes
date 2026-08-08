#!/usr/bin/env bash
set -euo pipefail

version="0.5.33"
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

grep -q '^0.5.33$' VERSION
grep -q '^version = "0.5.33"$' zumbra.toml
grep -q '^version = "0.5.33"$' zumbra-app.toml

git diff --quiet -- . || {
  echo "Working tree has uncommitted changes. Commit before tagging." >&2
  exit 1
}

git tag -a "v$version" -m "zumbra-nes $version"
echo "Created tag v$version"
echo "Push with: git push origin main --tags"
