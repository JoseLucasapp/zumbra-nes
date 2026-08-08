#!/usr/bin/env bash
set -euo pipefail

git status --short
git add .
git commit -m "release: zumbra-nes 0.5.34 CPU hot-loop performance"
git tag -a v0.5.34 -m "zumbra-nes 0.5.34"
git push origin main --tags
