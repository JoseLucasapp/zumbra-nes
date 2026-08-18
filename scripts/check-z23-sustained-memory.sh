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

var data << readBytes("fixtures/synthetic/visible-frame.nes");
var cart << cartridge.fromBytes(data, "fixtures/synthetic/visible-frame.nes");
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
    panic("sustained memory grew by " + toString(delta) + " bytes");
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

# Native achievement lifetime regression. Do not gate on exact source spelling here:
# formatting/refactors can legitimately change desktop.zum while preserving behavior.
# The compiled native probe below is the source of truth for cache lifetime and
# SQLite-backed numeric values.
achievement_probe="$work/achievement_lifetime.zum"
cat > "$achievement_probe" <<'ZUM'
import "../../src/achievements/engine.zum" as achievements;
import "../../src/achievements/offline.zum" as offline;
import "../../src/core/cartridge.zum" as cartridge;
import "../../src/core/console.zum" as console;
import "../../src/persistence/store.zum" as store;

var db << store.memory();
var cart << cartridge.load("fixtures/synthetic/nrom-128-horizontal.nes");
var machine << console.create(cart);
var digest << cart["info"].digest;
offline.install(db, cart["info"], 1u64);

var cacheBase << runtimeMemoryMark();
var rows << offline.rows(db, digest);
var summary << offline.summary(db, digest);
var unlockedCount << toInt(summary["unlocked"]);
var totalCount << toInt(summary["total"]);
var frameMark << runtimeMemoryMark();

var unlockedNow << achievements.evaluate(db, digest, machine, 1, 1, 0, 2u64);
var unlockedNowCount << sizeOf(unlockedNow);
if (unlockedNowCount <= 0) {
    panic("achievement lifetime probe expected an unlock");
}

runtimeMemoryReset(cacheBase);
rows << offline.rows(db, digest);
summary << offline.summary(db, digest);
unlockedCount << toInt(summary["unlocked"]);
totalCount << toInt(summary["total"]);
frameMark << runtimeMemoryMark();

if (sizeOf(rows) != 5) {
    panic("achievement lifetime probe lost achievement rows");
}
var firstRow << rows[0];
var firstRowProgress << toInt(firstRow["progress"]);
var firstRowTarget << toInt(firstRow["target"]);
if (firstRowProgress < 0 or firstRowTarget <= 0) {
    panic("achievement row numeric normalization failed");
}
if (unlockedCount != 2) {
    panic("achievement lifetime probe expected first-frame + first-input unlocks");
}
if (unlockedCount >= totalCount) {
    panic("achievement lifetime probe expected locked achievements to remain");
}

runtimeMemoryReset(frameMark);
if (toInt(summary["unlocked"]) != 2) {
    panic("cached achievement summary did not survive frame reset");
}
store.close(db);
show("achievement-lifetime: ok");
show(unlockedCount);
show(totalCount);
ZUM

"$zumbra_bin" build --release "$achievement_probe" -o "$work/achievement-lifetime"
"$work/achievement-lifetime" | awk '!/^semantic warning in /' | tee "$work/achievement-output.txt"
grep -q '^achievement-lifetime: ok$' "$work/achievement-output.txt"
grep -q '^2$' "$work/achievement-output.txt"
grep -q '^5$' "$work/achievement-output.txt"

