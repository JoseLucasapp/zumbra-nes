#!/usr/bin/env bash
set -euo pipefail

git status --short
git add .
git commit -m "release: zumbra-nes 0.5.35 smooth fast ppu"
git tag -a v0.5.35 -m "zumbra-nes 0.5.35"
git push origin main --tags
