#!/usr/bin/env bash
set -euo pipefail

git tag -a v0.5.40 -m "zumbra-nes 0.5.40"
git push origin main --tags
