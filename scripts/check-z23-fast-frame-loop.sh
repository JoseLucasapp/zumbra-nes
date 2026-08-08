#!/usr/bin/env bash
set -euo pipefail

zumbra_bin="${1:-${ZUMBRA_BIN:-zumbra}}"
command -v "$zumbra_bin" >/dev/null 2>&1 || { echo "Zumbra CLI not found: $zumbra_bin" >&2; exit 1; }

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

work="build/z23-fast-frame"
rm -rf "$work"
mkdir -p "$work"
probe="$work/z23_fast_frame_loop.zum"
cat > "$probe" <<'ZUM'
import "../../src/core/cartridge.zum" as cartridge;
import "../../src/core/console.zum" as console;
import "../../src/core/palette.zum" as palette;

var data << readBytes("fixtures/homebrew/zebra-platformer.nes");
var cart << cartridge.fromBytes(data, "fixtures/homebrew/zebra-platformer.nes");
var machine << console.create(cart);
var rgba << palette.rgbaBuffer(machine["bus"]["ppu"]["framebuffer"]);
console.setPerformanceMode(machine, true);
var mark << runtimeMemoryMark();
runtimeMemoryResetPeak();
var frames << 0;
var slices << 0;
while (frames < 180) {
    console.clearFrameComplete(machine);
    var inner << 0;
    while (!console.frameComplete(machine) and inner < 16) {
        console.runFrameSliceCode(machine, 65536);
        if ((inner % 8) == 0) {
            runtimeMemoryReset(mark);
        }
        inner << inner + 1;
        slices << slices + 1;
    }
    if (!console.frameComplete(machine)) {
        panic("Z23 fast frame loop did not complete a frame inside 16 slices");
    }
    if ((frames % 2) == 0) {
        console.renderFrameSnapshot(machine);
        palette.writeRgba(machine["bus"]["ppu"]["framebuffer"], rgba);
    }
    runtimeMemoryReset(mark);
    frames << frames + 1;
}
runtimeMemoryReset(mark);
show("z23-fast-frame-loop: ok");
show(frames);
show(slices);
ZUM

"$zumbra_bin" build --release "$probe" -o "$work/z23-fast-frame-loop"
"$work/z23-fast-frame-loop" | awk '!/^semantic warning in /' | tee "$work/output.txt"
grep -q '^z23-fast-frame-loop: ok$' "$work/output.txt"
grep -q '^180$' "$work/output.txt"
