# zumbra-nes 0.5.40

Input UX and Xbox controller release.

## Changes

- Moves the editable controls screen into the emulator window through an in-frame overlay.
- Stops printing the controls menu repeatedly to the terminal.
- Makes `1` through `8` remap buttons only while the Settings overlay is open.
- Adds an input-release lock after ROM/start/settings transitions to avoid stuck Enter/D-pad state.
- Keeps keyboard bindings editable and persisted in `zumbra-nes-controls.json`.
- Adds automatic gamepad polling for Xbox-style controllers through the Zumbra desktop runtime.
- Keeps hidden keyboard aliases and automatic Select+Start injection disabled.

## Default keyboard controls

- A: `Z`
- B: `X`
- Select: `Tab`
- Start: `Enter`
- D-pad: arrow keys
- F1: Settings overlay
- F2: reset controls while Settings is visible
- Esc: close/cancel

## Default Xbox-style gamepad mapping

- NES A: south/Xbox A or west/Xbox X
- NES B: east/Xbox B or north/Xbox Y
- Select: back/view
- Start: menu/start
- D-pad: gamepad D-pad
