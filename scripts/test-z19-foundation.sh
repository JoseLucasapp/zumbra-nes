#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Z19 is preserved by tag v0.1.0. The current tree is Z20/0.2.0; running the current gate."
exec "$root/scripts/test-z20-cpu.sh" "$@"
