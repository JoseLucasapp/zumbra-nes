# zumbra-nes 0.5.45

CI hygiene version fix.

## Changes

- Removes hardcoded zumbra-nes version checks from release scripts.
- Reads package/test/hygiene version from VERSION.
- Keeps AppImage optional when appimagetool is unavailable.
- Preserves 0.5.43/0.5.44 input, audio, settings and Linux packaging behavior.
