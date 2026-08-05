# zumbra-nes 0.5.20 — safe shell, input guard and Mapper 227 throttle

This release treats the 1200-in-1 Mapper 227 ROM as a host-safety problem first.
The previous builds could keep the host CPU busy while the ROM stayed in a black
screen path, making the desktop unresponsive. This version intentionally favors
not freezing the computer over trying to brute-force the multicart.

## Changes

- Replaces the synthetic controller hold with direct live input masks, fixing the
  issue where one Down tap could continue scrolling automatically.
- Adds a startup menu panel with the emulator shortcuts for games, controls,
  video/GPU options, execution/CPU controls and recent library entries.
- Changes the no-ROM startup behavior: the emulator now opens to the menu instead
  of forcing the file picker immediately.
- Simplifies the intro to a still Zumbra logo screen.
- Reduces Mapper 227 desktop execution to very small cooperative slices.
- Adds a no-frame watchdog for Mapper 227: if no frame is produced for a long
  interval, emulation pauses instead of locking the whole PC.
- Adds a mandatory host delay for Mapper 227 so the window manager and keyboard
  remain responsive.

## Known limitations

Mapper 227 remains experimental. Some 1200-in-1 internal game selections may still
not boot correctly until the mapper behavior is corrected further. The acceptance
bar for this release is that the emulator must not trap the user in an infinite
scroll, must not consume the whole desktop, and must pause safely instead of being
killed by the OS.
