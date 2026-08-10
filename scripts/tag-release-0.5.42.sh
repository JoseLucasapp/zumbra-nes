#!/usr/bin/env bash
set -euo pipefail
git tag -fa v0.5.42 -m "zumbra-nes 0.5.42"
git push --force origin v0.5.42
