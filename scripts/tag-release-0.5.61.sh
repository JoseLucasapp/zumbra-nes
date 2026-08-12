#!/usr/bin/env bash
set -euo pipefail

git tag -fa v0.5.61 -m "zumbra-nes 0.5.61"
git push --force origin v0.5.61
