# Zumbra NES 0.5.10 — Mapper 227 low-latency performance hotfix

This hotfix targets the real `1200-in-1.nes` Mapper 227 menu on Linux desktop.

Changes:

- keeps Zumbra language at `0.14.3`;
- disables APU ticking for Mapper 227 because audio is intentionally muted for this board family;
- preserves PPU timing/NMI but skips expensive visible scanline rendering on intermediate Mapper 227 frames;
- runs one full-frame Mapper 227 burst per host loop instead of tiny slices;
- extends short host key taps so the ROM can read the NES controller serially;
- keeps SDL event polling before and after emulation bursts;
- explicitly accepts Right Shift as Select in addition to Left Shift, Tab and Backspace.

The goal is to reduce menu input latency from minute-scale to usable host-input latency while the emulator remains a pure Zumbra/C11 build.
