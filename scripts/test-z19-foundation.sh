#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

zumbra_bin="${ZUMBRA_BIN:-zumbra}"
expected_version="${EXPECTED_ZUMBRA_VERSION:-0.14.1}"

if ! command -v "$zumbra_bin" >/dev/null 2>&1; then
    echo "Zumbra CLI not found: $zumbra_bin" >&2
    echo "Set ZUMBRA_BIN=/absolute/path/to/zumbra when it is not in PATH." >&2
    exit 1
fi

actual_version="$($zumbra_bin --version)"
if [[ "$actual_version" != "$expected_version" ]]; then
    echo "Zumbra version mismatch: expected $expected_version, got $actual_version" >&2
    exit 1
fi

echo "Running Z19 foundation gate with Zumbra $actual_version..."

mkdir -p build
sha256sum -c fixtures/SHA256SUMS
"$zumbra_bin" fmt --check src tests
"$zumbra_bin" lint --deny-warnings --no-pipeline --no-public-docs --max-line-length 400 src tests
"$zumbra_bin" project info
"$zumbra_bin" project check
"$zumbra_bin" project test
"$zumbra_bin" project doc
"$zumbra_bin" project run

if [[ "${Z19_SKIP_NATIVE:-0}" != "1" ]]; then
    "$zumbra_bin" project build -o build/zumbra-nes
    ./build/zumbra-nes > build/native-smoke.txt
    grep -q 'Zumbra NES Z19 foundation' build/native-smoke.txt
    grep -q '^32768$' build/native-smoke.txt
fi

scripts/check-repository-hygiene.sh

echo "Z19 foundation gate passed."
