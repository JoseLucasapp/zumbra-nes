#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

zumbra_bin="${ZUMBRA_BIN:-zumbra}"
expected_version="${EXPECTED_ZUMBRA_VERSION:-0.14.3}"

command -v "$zumbra_bin" >/dev/null 2>&1 || { echo "Zumbra CLI not found: $zumbra_bin" >&2; exit 1; }
actual_version="$($zumbra_bin --version)"
[[ "$actual_version" == "$expected_version" ]] || { echo "Zumbra version mismatch: expected $expected_version, got $actual_version" >&2; exit 1; }

echo "Running Z22 playable emulator gate with Zumbra $actual_version..."
rm -rf build dist
mkdir -p build dist

sha256sum -c fixtures/SHA256SUMS
python3 scripts/verify-cpu-table.py
"$zumbra_bin" fmt --check src tests
"$zumbra_bin" lint --deny-warnings --no-pipeline --no-public-docs --max-line-length 400 src tests
"$zumbra_bin" project info | tee build/project-info.txt
grep -q '^project: Zumbra NES$' build/project-info.txt
grep -q '^version: 0.4.0$' build/project-info.txt
"$zumbra_bin" project check
"$zumbra_bin" project test | tee build/project-tests.txt
grep -q '^project test: 55 test file(s) executed$' build/project-tests.txt
"$zumbra_bin" project doc

"$zumbra_bin" project run > build/vm-run-raw.txt
awk '!/^semantic warning in /' build/vm-run-raw.txt > build/vm-smoke.txt
cat build/vm-smoke.txt
mapfile -t smoke < build/vm-smoke.txt
[[ "${smoke[0]:-}" == "Zumbra NES Z22 playable" ]]
[[ "${smoke[1]:-}" == "0.4.0" ]]
[[ "${smoke[2]:-}" == "0" ]]
[[ "${smoke[4]:-}" == "245760" ]]
[[ "${#smoke[5]}" -eq 64 ]]
[[ "${#smoke[7]}" -eq 64 ]]
[[ "${smoke[8]:-}" == "3" ]]
[[ "${smoke[9]:-}" == "1" ]]
[[ "${smoke[10]:-}" == "1" ]]

if [[ "${Z22_SKIP_NATIVE:-0}" != "1" ]]; then
    "$zumbra_bin" project build -o build/zumbra-nes-headless
    ./build/zumbra-nes-headless > build/native-smoke.txt
    diff -u build/vm-smoke.txt build/native-smoke.txt

    "$zumbra_bin" app doctor --manifest zumbra-app.toml --target linux --arch amd64 --format appdir --json > build/app-doctor.json
    grep -q '"ready": true' build/app-doctor.json
    "$zumbra_bin" app build --manifest zumbra-app.toml --target linux --arch amd64 --release -o build/zumbra-nes
    ZUMBRA_DESKTOP_HEADLESS=1 ./build/zumbra-nes > build/desktop-smoke.txt
    grep -q '^Z22 desktop session complete$' build/desktop-smoke.txt
    grep -q '^2$' build/desktop-smoke.txt

    if [[ "${Z22_SKIP_PACKAGES:-0}" != "1" ]]; then
        Z22_PACKAGE_DIR=dist scripts/package-z22-linux.sh
    fi
fi

scripts/check-repository-hygiene.sh

echo "Z22 playable emulator gate passed."
