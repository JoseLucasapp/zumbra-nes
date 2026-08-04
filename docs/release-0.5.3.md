# Zumbra NES 0.5.3 — native-safe multicart input hotfix

This hotfix keeps the language requirement at Zumbra 0.14.3 and avoids the typed PPU/APU native path that caused the 0.5.2 headless native smoke to fail with `field access requires a struct or enum type`.

## Fixes

- Restores the stable dictionary-based PPU/APU core path from 0.5.1.
- Keeps the Mapper 227 desktop idle throttle.
- Keeps fallback keyboard aliases for multicart menus:
  - Start: Enter, Space, keypad Enter
  - Select: Right Shift, Left Shift, Tab, Backspace
  - D-pad: Arrow keys or WASD
  - A/B: Z/X or J/K
- Keeps Zumbra-lang pinned to 0.14.3.

## Validation expected on Debian

```bash
EXPECTED_ZUMBRA_VERSION=0.14.3 scripts/test-z23-compatibility.sh
./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"
```
