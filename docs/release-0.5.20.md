# Zumbra NES 0.5.20

Z23 safety reset release.

This release removes the persistent settings/store shell from the live desktop startup path and boots through a minimal SDL shell first. It is intended to prove that the executable can open, present the Zumbra intro, close with Esc, and run ROMs without freezing the host.

Changes:

- No-ROM startup now uses a minimal safe shell instead of the experimental menu/settings path.
- The intro is presented before any local database/settings work.
- The runtime player-one input mask is hard-coded in the live loop to avoid stuck synthetic holds.
- Mapper 227 runs in smaller cooperative slices and yields to the host on every pass.
- Local persistence, achievements, remapping UI, and rich menus are temporarily bypassed in the live desktop path until the emulator shell is stable.

Validation target:

- `./build/zumbra-nes` opens and shows the Zumbra intro/shell.
- Esc closes the process quickly.
- `taskset -c 0 ./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"` must not freeze the full desktop.
