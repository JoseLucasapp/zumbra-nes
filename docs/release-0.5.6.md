# Zumbra NES 0.5.6 — Mapper 227 input latency hotfix

This release is a targeted Z23 hotfix for the real `1200-in-1.nes` Mapper 227 menu.

## Fixed

- Added a short host-side controller hold window so quick key taps are not lost between SDL polling and NES controller polling.
- Increased the Mapper 227 execution slice so menu input is sampled and rendered at interactive speed.
- Increased the temporary input burst while a key is pressed or recently pressed.
- Kept Mapper 227 audio muted by default from 0.5.5 to avoid unstable noise until APU timing receives its own compatibility pass.

## Language compatibility

- Requires Zumbra `0.14.3`.
- No Zumbra language changes are included.

## Validation

Run:

```bash
EXPECTED_ZUMBRA_VERSION=0.14.3 scripts/test-z23-compatibility.sh
```

Then test the real ROM manually:

```bash
./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"
```
