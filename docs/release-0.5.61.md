# zumbra-nes 0.5.61

Z28 compatibility and mapper expansion.

## Changes

- Expands the supported mapper registry from 8 to 15 mapper families.
- Adds Mapper 11 / Color Dreams PRG+CHR bank switching.
- Adds Mapper 30 / UNROM 512 PRG bank switching and one-screen mirroring selection.
- Adds Mapper 66 / GxROM PRG+CHR bank switching.
- Adds Mapper 71 / Camerica/Codemasters PRG bank switching and one-screen mirroring control.
- Adds Mapper 87 / Jaleco JF-13 CHR banking with swapped select bits.
- Adds Mapper 94 / UN1ROM shifted PRG bank selection.
- Adds Mapper 180 / UNROM reverse high-bank switching.
- Adds a Z28 compatibility matrix document.
- Adds mapper expansion and diagnostics regression tests.
- Keeps Zumbra-lang pinned to 0.14.5.
- Keeps Z27 typed settings, audio ON/OFF, remaps, recent ROM, quick save/load and desktop UX intact.

## Validation

Run:

```bash
EXPECTED_ZUMBRA_VERSION=0.14.5 scripts/test-z23-compatibility.sh
```

Expected final line:

```text
Z28 compatibility, mapper expansion, persistence and debugger gate passed.
```
