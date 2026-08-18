#!/usr/bin/env bash
set -euo pipefail

if [[ -n "$(git status --porcelain)" ]]; then
    echo "Refusing to tag: working tree is not clean." >&2
    exit 1
fi

if git rev-parse -q --verify refs/tags/v0.5.63 >/dev/null; then
    echo "Refusing to tag: v0.5.63 already exists." >&2
    exit 1
fi

git tag -a v0.5.63 -m "zumbra-nes 0.5.63"
git push origin v0.5.63
