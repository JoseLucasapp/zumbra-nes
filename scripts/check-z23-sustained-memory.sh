#!/usr/bin/env bash
set -euo pipefail

zumbra_bin="${1:-${ZUMBRA_BIN:-zumbra}}"
command -v "$zumbra_bin" >/dev/null 2>&1 || { echo "Zumbra CLI not found: $zumbra_bin" >&2; exit 1; }

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

work="build/z23-memory"
rm -rf "$work"
mkdir -p "$work"
probe="$work/z23_memory_hotloop.zum"
cat > "$probe" <<'ZUM'
import "../../src/core/cartridge.zum" as cartridge;
import "../../src/core/console.zum" as console;
import "../../src/core/palette.zum" as palette;

var data << readBytes("fixtures/synthetic/z23-visible-frame.nes");
var cart << cartridge.fromBytes(data, "fixtures/synthetic/z23-visible-frame.nes");
var machine << console.create(cart);
var rgba << palette.rgbaBuffer(machine["bus"]["ppu"]["framebuffer"]);
var before << runtimeMemoryStats();
var baseline << toInt(before["activeBytes"]);
var mark << runtimeMemoryMark();
runtimeMemoryResetPeak();
var frames << 0;
var slices << 0;
while (frames < 120) {
    console.clearFrameComplete(machine);
    var inner << 0;
    while (!console.frameComplete(machine) and inner < 512) {
        console.runFrameSliceCode(machine, 512);
        runtimeMemoryReset(mark);
        inner << inner + 1;
        slices << slices + 1;
    }
    palette.writeRgba(machine["bus"]["ppu"]["framebuffer"], rgba);
    runtimeMemoryReset(mark);
    frames << frames + 1;
}
runtimeMemoryReset(mark);
var after << runtimeMemoryStats();
var active << toInt(after["activeBytes"]);
var delta << active - baseline;
if (delta < 0) {
    delta << 0;
}
if (delta > 524288) {
    panic("Z23 sustained memory grew by " + toString(delta) + " bytes");
}
show("z23-memory-hotloop: ok");
show(frames);
show(slices);
show(delta);
ZUM

"$zumbra_bin" build --release "$probe" -o "$work/z23-memory-hotloop"
"$work/z23-memory-hotloop" | awk '!/^semantic warning in /' | tee "$work/output.txt"
grep -q '^z23-memory-hotloop: ok$' "$work/output.txt"
grep -q '^120$' "$work/output.txt"
