# zumbra-nes 0.5.61

**Z28 compatibility and mapper expansion:** the emulator now supports 15 mapper families while keeping the Zumbra-lang baseline frozen at **0.14.5**. Z27 typed settings persistence, recent ROM persistence, audio ON/OFF, controller remaps, quick save/load and the desktop UX remain intact.

Zumbra NES is a local-first NES/Famicom emulator written in **Zumbra**. The application repository keeps the emulator code in `.zum`; video, audio, input, packaging and desktop integration come from the official Zumbra runtime.

No commercial ROM is included.

## Compatibility

Supported mappers:

- `0` — NROM;
- `1` — MMC1/SxROM;
- `2` — UxROM;
- `3` — CNROM;
- `4` — MMC3/TxROM;
- `7` — AxROM;
- `10` — MMC4/FxROM;
- `11` — Color Dreams;
- `30` — UNROM 512;
- `66` — GxROM;
- `71` — Camerica/Codemasters;
- `87` — Jaleco JF-13;
- `94` — UN1ROM;
- `180` — UNROM reverse;
- `227` — multicart/address-latch boards.

The implementation covers common iNES behavior for those families. Specific board revisions, copy-protection behavior, unusual submappers, extra audio chips and ROMs depending on unofficial 6502 opcodes may still require future compatibility work.

See `docs/compatibility-matrix-z28.md` and `docs/mappers-z23.md` for mapper details.

## Features

- iNES 1.0 and basic NES 2.0 header detection;
- CPU Ricoh 2A03 with the 151 official opcodes;
- PPU 2C02 background, sprites, scrolling, VBlank/NMI and OAM DMA;
- APU pulse 1/2, triangle, noise and DMC;
- keyboard and gamepad input;
- SQLite-backed local settings and ROM history;
- SRAM persistence;
- ten save-state slots;
- debugger with stepping, breakpoints, memory inspection and mapper state;
- Linux AppDir and `.deb` packaging;
- AppImage optional when `appimagetool` is available.

## Requirements

- Linux amd64;
- Zumbra `0.14.5`;
- Clang or GCC;
- `libsqlite3-0`;
- `libsdl3-0` for the desktop frontend;
- `zenity` recommended for the ROM picker;
- `appimagetool` optional.

```bash
zumbra --version
```

Expected:

```text
0.14.5
```

## Build

```bash
zumbra app build \
  --manifest zumbra-app.toml \
  --target linux \
  --arch amd64 \
  --release \
  -o build/zumbra-nes
```

Open the launcher:

```bash
./build/zumbra-nes
```

Open a ROM you own:

```bash
./build/zumbra-nes /path/to/game.nes
```

Run the legal visual fixture:

```bash
./build/zumbra-nes fixtures/synthetic/z23-visible-frame.nes
```

## Gate

```bash
EXPECTED_ZUMBRA_VERSION=0.14.5 \
  scripts/test-z23-compatibility.sh
```

The gate validates:

- fixture checksums;
- CPU opcode table;
- formatter and linter;
- project info/check diagnostics;
- 79 direct test files;
- docs generation;
- VM smoke;
- native C11 smoke;
- sustained memory and fast-frame hot loops;
- desktop app doctor;
- desktop headless smoke;
- unsupported mapper diagnostics;
- AppDir and `.deb` packaging;
- repository hygiene.

Expected final line:

```text
Z28 compatibility, mapper expansion, persistence and debugger gate passed.
```

## Packaging

```bash
scripts/package-z23-linux.sh
```

Main artifacts:

```text
dist/zumbra-nes-0.5.61-linux-amd64.AppDir/
dist/zumbra-nes_0.5.61_amd64.deb
```

## Current status

```text
Zumbra-lang baseline: 0.14.5
zumbra-nes release: 0.5.61
phase: Z28 compatibility and mapper expansion
supported mappers: 15
```
