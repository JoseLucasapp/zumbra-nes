#!/usr/bin/env bash
set -euo pipefail

git tag -fa v0.5.40 -m "zumbra-nes 0.5.40"
git push --force origin v0.5.40
