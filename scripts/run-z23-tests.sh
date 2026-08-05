#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

zumbra_bin="${1:-zumbra}"
mkdir -p build

mapfile -t test_files < <(find tests -maxdepth 1 -type f -name '*_test.zum' | LC_ALL=C sort)
: > build/project-tests.txt

for test_file in "${test_files[@]}"; do
    echo "test $root/$test_file" | tee -a build/project-tests.txt
    if ! "$zumbra_bin" run "$test_file" 2>&1 | tee -a build/project-tests.txt; then
        echo "test $test_file failed" | tee -a build/project-tests.txt >&2
        exit 1
    fi
done

echo "project test: ${#test_files[@]} test file(s) executed" | tee -a build/project-tests.txt
