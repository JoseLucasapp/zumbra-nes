#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

zumbra_bin="${ZUMBRA_BIN:-zumbra}"
expected_version="${EXPECTED_ZUMBRA_VERSION:-0.14.2}"

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

echo "Running Z20 CPU 6502 gate with Zumbra $actual_version..."

rm -rf build
mkdir -p build

sha256sum -c fixtures/SHA256SUMS
python3 scripts/verify-cpu-table.py
"$zumbra_bin" fmt --check src tests
"$zumbra_bin" lint --deny-warnings --no-pipeline --no-public-docs --max-line-length 400 src tests
"$zumbra_bin" project info | tee build/project-info.txt
grep -q '^project: Zumbra NES$' build/project-info.txt
grep -q '^version: 0.2.0$' build/project-info.txt
"$zumbra_bin" project check
"$zumbra_bin" project test | tee build/project-tests.txt
grep -q '^project test: 23 test file(s) executed$' build/project-tests.txt
"$zumbra_bin" project doc

# `project run` currently emits non-fatal semantic warnings on stdout.
# Preserve the raw output for diagnostics and normalize only the smoke output
# used by deterministic assertions and VM/native parity.
"$zumbra_bin" project run > build/vm-run-raw.txt
awk '!/^semantic warning in /' build/vm-run-raw.txt > build/vm-smoke.txt
cat build/vm-smoke.txt

mapfile -t smoke < build/vm-smoke.txt
[[ "${smoke[0]:-}" == "Zumbra NES Z20 CPU 6502" ]]
[[ "${smoke[2]:-}" == "iNES 1.0" ]]
[[ "${smoke[3]:-}" == "0" ]]
[[ "${smoke[7]:-}" == "32768" ]]
[[ "${smoke[8]:-}" == "1" ]]
[[ "${smoke[12]:-}" == "32771" ]]
[[ "${smoke[14]:-}" == "2" ]]
[[ "${smoke[15]:-}" == "11" ]]
[[ "${smoke[16]:-}" == "11" ]]
[[ "${smoke[17]:-}" == "33" ]]

if [[ "${Z20_SKIP_NATIVE:-0}" != "1" ]]; then
    "$zumbra_bin" project build -o build/zumbra-nes
    test -x build/zumbra-nes
    ./build/zumbra-nes > build/native-smoke.txt
    cat build/native-smoke.txt
    diff -u build/vm-smoke.txt build/native-smoke.txt
fi

scripts/check-repository-hygiene.sh

echo "Z20 CPU 6502 gate passed."
