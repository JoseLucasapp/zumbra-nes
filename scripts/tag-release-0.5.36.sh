#!/usr/bin/env bash
set -euo pipefail

git status --short
git add .
git commit -m "release: zumbra-nes 0.5.40 input hotfix"
git tag -a v0.5.40 -m "zumbra-nes 0.5.40"
git push origin main --tags
