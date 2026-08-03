#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "Z19 is preserved by tag v0.1.0. The current tree is Z21/0.3.0; running the current gate."
exec "$root/scripts/test-z21-hardware.sh" "$@"
