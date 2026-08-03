#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

for forbidden in .env '*.key' '*.pem' '*.p12' '*.pfx'; do
    if find . -path './.git' -prune -o -name "$forbidden" -print | grep -q .; then
        echo "Forbidden secret-like file found: $forbidden" >&2
        exit 1
    fi
done

unexpected_roms="$(find . -path './.git' -prune -o \( -iname '*.nes' -o -iname '*.fds' -o -iname '*.unf' -o -iname '*.unif' \) -type f ! -path './fixtures/synthetic/*' -print)"
if [[ -n "$unexpected_roms" ]]; then
    echo "ROM images are allowed only under fixtures/synthetic:" >&2
    printf '%s\n' "$unexpected_roms" >&2
    exit 1
fi

while IFS= read -r rom; do
    size="$(stat -c '%s' "$rom")"
    if (( size > 131072 )); then
        echo "Synthetic ROM is unexpectedly large: $rom ($size bytes)" >&2
        exit 1
    fi
done < <(find fixtures/synthetic -type f -iname '*.nes' -print)

if [[ -d .git ]]; then
    tracked_generated="$(git ls-files 'build/**' 'dist/**' '.zumbra/**')"
    if [[ -n "$tracked_generated" ]]; then
        echo "Generated files are tracked:" >&2
        printf '%s\n' "$tracked_generated" >&2
        exit 1
    fi
fi

echo "Z19 repository hygiene checks passed."
