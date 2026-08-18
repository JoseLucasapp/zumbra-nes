#!/usr/bin/env bash
set -euo pipefail

if [[ -n "$(git status --porcelain)" ]]; then
    echo "Refusing to tag: working tree is not clean." >&2
    exit 1
fi

[[ "$(cat VERSION)" == "0.5.64" ]] || { echo "VERSION is not 0.5.64" >&2; exit 1; }
if git rev-parse -q --verify refs/tags/v0.5.64 >/dev/null; then
    echo "Refusing to tag: v0.5.64 already exists." >&2
    exit 1
fi

git tag -a v0.5.64 -m "zumbra-nes 0.5.64"
git push origin v0.5.64
