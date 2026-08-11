#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

project_version="$(cat VERSION)"

for forbidden in .env '*.key' '*.pem' '*.p12' '*.pfx' '*.sqlite' '*.sqlite3' '*.db' '*.sav' '*.zst'; do
    if find . -path './.git' -prune -o -path './build' -prune -o -path './dist' -prune -o -path './zumbra-nes.sqlite3' -prune -o -name "$forbidden" -print | grep -q .; then
        echo "Forbidden secret or generated persistence file found: $forbidden" >&2
        exit 1
    fi
done

unexpected_roms="$(find . -path './.git' -prune -o \( -iname '*.nes' -o -iname '*.fds' -o -iname '*.unf' -o -iname '*.unif' \) -type f ! -path './fixtures/synthetic/*' ! -path './fixtures/homebrew/*' -print)"
if [[ -n "$unexpected_roms" ]]; then
    echo "ROM images are allowed only under fixtures/synthetic or fixtures/homebrew:" >&2
    printf '%s\n' "$unexpected_roms" >&2
    exit 1
fi

while IFS= read -r rom; do
    size="$(stat -c '%s' "$rom")"
    if (( size > 1048576 )); then
        echo "Synthetic ROM is unexpectedly large: $rom ($size bytes)" >&2
        exit 1
    fi
done < <(find fixtures/synthetic fixtures/homebrew -type f -iname '*.nes' -print)

grep -q "^version = \"${project_version}\"$" zumbra.toml
grep -q "^version = \"${project_version}\"$" zumbra-app.toml
if find . -path './.git' -prune -o -path './build' -prune -o -path './dist' -prune -o -type f \( -name '*.c' -o -name '*.h' \) -print | grep -q .; then
    echo "Project-local C/C headers are forbidden; use the official Zumbra runtime." >&2
    exit 1
fi
if grep -R --include='*.zum' -n 'extern "C"' src tests >/dev/null 2>&1; then
    echo 'Project-local extern "C" declarations are forbidden.' >&2
    exit 1
fi
test -f assets/zumbra-nes.png
test -f fixtures/synthetic/mapper227-multicart.nes
test -f fixtures/synthetic/z23-visible-frame.nes
test -f src/core/mapper.zum
test -f src/persistence/save_ram.zum
test -f src/persistence/save_state.zum
test -f src/debugger/debugger.zum
test -x scripts/test-z23-compatibility.sh
test -x scripts/check-zumbra-native-performance.sh
test -x scripts/check-z23-sustained-memory.sh
test -x scripts/check-z23-fast-frame-loop.sh
test -x scripts/run-z23-tests.sh
test -x scripts/package-z23-linux.sh
test "$(find tests -maxdepth 1 -type f -name '*_test.zum' | wc -l)" -eq 77

if [[ -d .git ]]; then
    tracked_generated="$(git ls-files 'build/**' 'dist/**' '.zumbra/**')"
    if [[ -n "$tracked_generated" ]]; then
        echo "Generated files are tracked:" >&2
        printf '%s\n' "$tracked_generated" >&2
        exit 1
    fi
fi

echo "Zumbra NES repository hygiene checks passed."
