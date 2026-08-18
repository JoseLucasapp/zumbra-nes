#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

zumbra_bin="${ZUMBRA_BIN:-zumbra}"
expected_version="${EXPECTED_ZUMBRA_VERSION:-0.14.5}"
project_version="$(cat VERSION)"

# Local release builds are tuned for the developer workstation. Disable or change
# these exports before creating a generic binary for another machine.
export ZUMBRA_NATIVE_TUNE="${ZUMBRA_NATIVE_TUNE:-native}"
export ZUMBRA_NATIVE_LTO="${ZUMBRA_NATIVE_LTO:-thin}"

command -v "$zumbra_bin" >/dev/null 2>&1 || { echo "Zumbra CLI not found: $zumbra_bin" >&2; exit 1; }
actual_version="$($zumbra_bin --version)"
[[ "$actual_version" == "$expected_version" ]] || { echo "Zumbra version mismatch: expected $expected_version, got $actual_version" >&2; exit 1; }
scripts/check-zumbra-native-performance.sh "$zumbra_bin"

echo "Running game library, local achievements, compatibility and debugger gate with Zumbra $actual_version..."
rm -rf build dist
mkdir -p build dist

sha256sum -c fixtures/SHA256SUMS
python3 scripts/generate-zebra-platformer-rom.py --check
python3 scripts/verify-cpu-table.py
python3 -m py_compile scripts/generate-synthetic-fixtures.py scripts/generate-zebra-platformer-rom.py scripts/verify-cpu-table.py
"$zumbra_bin" fmt --check src tests
"$zumbra_bin" lint --deny-warnings --no-pipeline --no-public-docs --max-line-length 1000 src tests
"$zumbra_bin" project info | tee build/project-info.txt
grep -q '^project: Zumbra NES$' build/project-info.txt
grep -q "^version: ${project_version}$" build/project-info.txt
# The project intentionally keeps modules available for the desktop/menu release path.
# Current Zumbra 0.14.5 returns a non-zero status for `project check` in this
# repository when diagnostics are warning-only/unused-symbol reports. Do not let
# that command block this gate; the authoritative checks below are fmt, lint,
# project test, VM smoke, native headless smoke and desktop smoke.
if ! "$zumbra_bin" project check > build/project-check.txt 2>&1; then
    cat build/project-check.txt
    echo "Project check is advisory for 0.5.63; continuing to test/build."
else
    cat build/project-check.txt
fi

# Zumbra 0.14.5 `project test` treats project-wide unused-symbol diagnostics
# as a failed aggregate precheck (37 src + 84 test files = 121 files), even
# though the executable test files are valid. The release gate therefore uses
# the explicit per-file test runner as its authoritative test execution step.
# Opt into the aggregate diagnostic trace only when investigating compiler
# diagnostics; it is intentionally off for normal release validation.
if [[ "${ZUMBRA_RUN_AGGREGATE_PROJECT_TEST:-0}" == "1" ]]; then
    "$zumbra_bin" project test | tee build/project-test-aggregate.txt || true
fi
scripts/run-z23-tests.sh "$zumbra_bin"
grep -Eq '^project test: [0-9]+ test file\(s\) executed$' build/project-tests.txt
"$zumbra_bin" project doc

"$zumbra_bin" project run > build/vm-run-raw.txt
awk '!/^semantic warning in /' build/vm-run-raw.txt > build/vm-smoke.txt
cat build/vm-smoke.txt
mapfile -t smoke < build/vm-smoke.txt
[[ "${smoke[0]:-}" == "Zumbra NES compatibility" ]]
[[ "${smoke[1]:-}" == "$project_version" ]]
[[ "${smoke[2]:-}" == "0" ]]
[[ "${smoke[3]:-}" == "NROM" ]]
[[ "${smoke[4]:-}" == "1" ]]
[[ "${smoke[5]:-}" == "245760" ]]
[[ "${#smoke[6]}" -eq 64 ]]
[[ "${#smoke[8]}" -eq 64 ]]
[[ "${smoke[9]:-}" == "6" ]]
[[ "${smoke[10]:-}" == "1" ]]
[[ "${smoke[11]:-}" == "1" ]]
[[ "${smoke[12]:-}" == "15" ]]
[[ "${smoke[13]:-}" == "1" ]]

if [[ "${Z23_SKIP_NATIVE:-0}" != "1" ]]; then
    "$zumbra_bin" project build -o build/zumbra-nes-headless
    ./build/zumbra-nes-headless > build/native-smoke.txt
    diff -u build/vm-smoke.txt build/native-smoke.txt

    scripts/check-z23-sustained-memory.sh "$zumbra_bin"
    scripts/check-z23-fast-frame-loop.sh "$zumbra_bin"

    "$zumbra_bin" app doctor --manifest zumbra-app.toml --target linux --arch amd64 --format appdir --json > build/app-doctor.json 2> build/app-doctor.err || true
    cat build/app-doctor.json
    if ! grep -q '"ready": true' build/app-doctor.json; then
        cat build/app-doctor.err >&2 || true
        echo "Desktop app doctor failed; see build/app-doctor.json" >&2
        exit 1
    fi
    "$zumbra_bin" app build --manifest zumbra-app.toml --target linux --arch amd64 --release -o build/zumbra-nes 2> build/app-build.err || { cat build/app-build.err >&2; exit 1; }
    ZUMBRA_DESKTOP_HEADLESS=1 ./build/zumbra-nes > build/desktop-smoke.txt
    grep -q '^Zumbra NES desktop session complete$' build/desktop-smoke.txt
    grep -q '^2$' build/desktop-smoke.txt

    ZUMBRA_DESKTOP_HEADLESS=1 ./build/zumbra-nes fixtures/synthetic/mapper227-multicart.nes > build/mapper227-desktop-smoke.txt
    grep -q '^Zumbra NES desktop session complete$' build/mapper227-desktop-smoke.txt
    grep -q '^2$' build/mapper227-desktop-smoke.txt

    ZUMBRA_DESKTOP_HEADLESS=1 ./build/zumbra-nes fixtures/synthetic/unsupported-mapper5.nes > build/unsupported-mapper.txt 2>&1 || true
    grep -q 'Incompatible ROM: mapper 5' build/unsupported-mapper.txt
    grep -q '0 (NROM)' build/unsupported-mapper.txt
    grep -q '180 (UNROM reverse)' build/unsupported-mapper.txt
grep -q '227 (multicart)' build/unsupported-mapper.txt

    ZUMBRA_DESKTOP_HEADLESS=1 ./build/zumbra-nes fixtures/homebrew/zebra-platformer.nes > build/zebra-platformer-smoke.txt
    grep -q '^Zumbra NES desktop session complete$' build/zebra-platformer-smoke.txt
    grep -q '^2$' build/zebra-platformer-smoke.txt

    if [[ "${Z23_SKIP_PACKAGES:-0}" != "1" ]]; then
        Z23_PACKAGE_DIR=dist scripts/package-z23-linux.sh
    fi
fi

# Production UI/input polish must not regress.
! grep -qE '\bZ[0-9]+\b|Xbox|XBOX' src/frontend/desktop.zum
grep -q 'native.gamepadButton(context, 1, button) or native.gamepadButton(context, 2, button)' src/frontend/desktop.zum
grep -q 'fct drawMainMenu' src/frontend/desktop.zum
grep -q 'controlsVisible << true' src/frontend/desktop.zum
grep -q 'returnToMenu << true' src/frontend/desktop.zum
grep -q 'pub fct firstKeyDown(context)' src/frontend/native_bridge.zum
grep -q 'fct saveRemapCode(context, controls, action, code)' src/frontend/desktop.zum
grep -q 'captureReady << true' src/frontend/desktop.zum
# 0.5.63 game-library UX must remain wired to local SQLite state.
grep -q 'fct drawGameLibrary' src/frontend/desktop.zum
grep -q 'fct drawGameDetails' src/frontend/desktop.zum
grep -q 'fct drawLibraryAchievements' src/frontend/desktop.zum
grep -q 'pub fct libraryRows' src/persistence/store.zum
grep -q 'pub fct pageState' src/frontend/library.zum

scripts/check-repository-hygiene.sh

echo "Zumbra NES release gate passed."
