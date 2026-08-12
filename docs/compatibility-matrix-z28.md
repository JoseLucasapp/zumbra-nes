# Z28 compatibility matrix

Z28 expands the mapper compatibility layer without changing the Zumbra-lang baseline. The emulator still targets Zumbra `0.14.5` and keeps the Z23 gate name for the long-running compatibility script.

## Supported mapper families

| Mapper | Family | PRG banking | CHR banking | Mirroring | Notes |
|---:|---|---|---|---|---|
| 0 | NROM | 16/32 KiB fixed | 8 KiB fixed/RAM | Header | Baseline fixture coverage. |
| 1 | MMC1/SxROM | 16/32 KiB serial register | 4/8 KiB | Register | PRG RAM enable and mapper snapshot covered. |
| 2 | UxROM | 16 KiB switchable + last fixed | CHR RAM/ROM fixed | Header | Existing Z23 coverage. |
| 3 | CNROM | NROM PRG | 8 KiB switchable | Header | Existing Z23 coverage. |
| 4 | MMC3/TxROM | 8 KiB windows | 1/2 KiB windows | Register | Scanline IRQ path covered. |
| 7 | AxROM | 32 KiB switchable | CHR RAM/ROM fixed | Single-screen | Existing Z23 coverage. |
| 10 | MMC4/FxROM | 16 KiB switchable + last fixed | 4 KiB latch banks | Register | Existing Z23/Z24 compatibility. |
| 11 | Color Dreams | 32 KiB switchable | 8 KiB switchable | Header | New Z28 discrete mapper. |
| 30 | UNROM 512 | 16 KiB switchable + last fixed | CHR RAM/ROM fixed | Single-screen bit | New Z28 mapper. |
| 66 | GxROM | 32 KiB switchable | 8 KiB switchable | Header | New Z28 discrete mapper. |
| 71 | Camerica/Codemasters | 16 KiB switchable + last fixed | CHR fixed | Single-screen register | New Z28 mapper. |
| 87 | Jaleco JF-13 | NROM PRG | 8 KiB switchable with swapped select bits | Header | New Z28 discrete mapper. |
| 94 | UN1ROM | 16 KiB switchable + last fixed | CHR fixed | Header | New Z28 mapper. |
| 180 | UNROM reverse | First 16 KiB fixed + high bank switchable | CHR fixed | Header | New Z28 mapper. |
| 227 | Multicart | Address-latch 16/32 KiB modes | CHR RAM protection | Address bit | Existing real-ROM focus. |

## Z28 acceptance

- `mapper.supportedCount()` must report `15`.
- Unsupported mapper diagnostics must include the expanded list.
- Existing audio, settings, input, save state and desktop behavior must remain untouched.
- The full gate must finish with `Z28 compatibility, mapper expansion, persistence and debugger gate passed.`
