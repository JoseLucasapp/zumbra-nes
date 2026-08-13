# zumbra-nes 0.5.62

Local achievements offline.

## Highlights

- Zumbra-lang remains pinned to `0.14.5`.
- Z28 compatibility and 15 mapper families remain intact.
- SQLite-backed local achievements, progress, unlock events and manual JSON backup remain fully offline.
- F6 renders real per-game rows; F9 exports JSON and E is the in-overlay fallback.
- All emulator-facing status/remap/compatibility text is English and production UI contains no development-phase labels.
- Procedural emulator-use achievements were removed from commercial-game fallback behavior.
- ROM recognition now uses SHA-256 plus local CRC-32 aliases for known revisions.
- Nintendo Tetris receives 8 Tetris-specific line/level/score goals.
- Nintendo Popeye receives 8 Popeye-specific score/round goals.
- Unknown games show `NO GAME-SPECIFIC PACK` until a semantic pack is added.
- Desktop audio keeps APU timing unchanged, clamps/compresses the byte stream to the safe 0.14.5 bridge range and resamples the /40 APU stream to 44.1 kHz at the output boundary.
- F3 now exposes live audio queue bytes and samples-per-frame for manual diagnosis.
- Controls from the main menu now opens the real remapping overlay; `1`-`8` remap, `F2` resets and `Esc` goes back.
- External controller handling is vendor-neutral through SDL Gamepad and polls both available 1-based runtime slots for automatic hot-plug input.
- Xbox-specific labels were removed.
- `Esc` is edge-triggered: it closes the current overlay or returns gameplay to the emulator menu; Quit/F12/window-close are explicit application exit paths.
- Gate remains 83 test files and schema version 5.

## Out of scope

- No online accounts.
- No cloud sync.
- No leaderboard.
- No remote achievement server.
- No web dependency for unlocks or viewing.
- No claim that arbitrary ROM machine code can automatically reveal semantic concepts such as score, boss, stage or collectibles.

## Gate

```text
project test: 83 test file(s) executed
Zumbra NES release gate passed.
```
