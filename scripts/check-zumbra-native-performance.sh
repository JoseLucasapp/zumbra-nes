#!/usr/bin/env bash
set -euo pipefail

zumbra_bin="${1:-${ZUMBRA_BIN:-zumbra}}"
command -v "$zumbra_bin" >/dev/null 2>&1 || { echo "Zumbra CLI not found: $zumbra_bin" >&2; exit 1; }

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"
mkdir -p build/perf-check
probe="build/perf-check/native_hotloop_probe.zum"
cat > "$probe" <<'ZUM'
struct Counter {
    value: int;
    fct add(amount) {
        self.value << (self.value + amount) band 255;
        self.value;
    }
}
fct hot(values) {
    var counter << Counter(0);
    var index << 0;
    while (index < sizeOf(values)) {
        counter.add(toInt(values[index]));
        index << index + 1;
    }
    show(counter.value);
}
hot(bytes(4));
ZUM
rm -rf build/perf-check/native
mkdir -p build/perf-check/native
(
    cd build/perf-check
    "$zumbra_bin" build --release --emit-c native_hotloop_probe.zum >/dev/null
)
main_c="build/perf-check/build/native/native_hotloop_probe/main.c"
if [[ ! -f "$main_c" ]]; then
    main_c="$(find build/perf-check -path '*/main.c' -print -quit)"
fi
if [[ -z "${main_c:-}" || ! -f "$main_c" ]]; then
    echo "Native performance check failed: generated C main.c not found." >&2
    exit 1
fi
missing=0
generated_dir="$(dirname "$main_c")"
for marker in 'z_gen_binary_op' 'z_gen_index_at' 'z_get_struct_field_at' 'z_string_static'; do
    if ! grep -R -q "$marker" "$generated_dir"; then
        echo "Native performance check failed: optimized marker not found: $marker" >&2
        missing=1
    fi
done
if grep -R -E 'z_get_field\([^,]+, "add"\)|z_get_field\([^,]+, "add"\)' "$generated_dir" >/dev/null 2>&1; then
    echo "Native performance check failed: method hot-loop still materializes Counter.add with z_get_field." >&2
    missing=1
fi
if ! grep -R -E 'zf_[0-9]+\(za_[0-9]+, 2\)' "$generated_dir" >/dev/null 2>&1; then
    echo "Native performance check failed: direct struct method call marker not found." >&2
    missing=1
fi
if (( missing != 0 )); then
    cat >&2 <<'MSG'
Install/apply the Zumbra 0.14.5 native performance/runtime patch, rebuild zumbra,
and make sure this project uses that rebuilt compiler before running the Z23 gate.
The public zumbra --version must be 0.14.5 for this release.
MSG
    exit 1
fi

echo "Zumbra native hot-loop performance checks passed."
