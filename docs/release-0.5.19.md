# zumbra-nes 0.5.20 — runtime field-access guard

Safety patch for the real SDL desktop frontend.

## Changes

- Avoids indexing raw desktop event payloads in `native.poll()`.
- Avoids `desktopPaths()` string-field indexing in the safety build.
- Disables platform notifications/panels in the startup path.
- Keeps startup on a stable title-bar shell: F1 menu, O open ROM, Esc exit.
- Keeps version 0.5.20 across manifest, scripts and docs.

## Acceptance

- `./build/zumbra-nes` opens without `field access requires a struct or enum type`.
- `Esc` closes the shell.
- `taskset -c 0 ./build/zumbra-nes ~/Downloads/1200-in-1.nes` does not freeze the desktop.
