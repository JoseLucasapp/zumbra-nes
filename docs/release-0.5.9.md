# Zumbra NES 0.5.9 — Mapper 227 Fast PPU Timing Hotfix

Hotfix focused on the real `1200-in-1.nes` Mapper 227 menu responsiveness.

The emulator remains built with Zumbra 0.14.3. No language/runtime update is required.

## Changes

- Added a fast PPU timing path for non-visible Mapper 227 frames.
- Kept the normal PPU path for visible frames and non-Mapper-227 ROMs.
- Increased host input retention for player 1 so short keyboard taps survive slow emulation turns.
- Rendered the Mapper 227 menu more sparsely while preserving VBlank/NMI timing on skipped frames.
- Kept Mapper 227 audio muted until the APU/timing milestone.

## Validation target

```bash
EXPECTED_ZUMBRA_VERSION=0.14.3 scripts/test-z23-compatibility.sh
./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"
```
