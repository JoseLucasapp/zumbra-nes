# zumbra-nes 0.5.40

Input settings release for the Z23 NES/Famicom desktop frontend.

## Changes

- Adds runtime controller settings for player 1.
- Press F1 during gameplay to view the current bindings in the title bar and terminal.
- Press 1-8 during gameplay to remap A, B, Select, Start, Up, Down, Left or Right.
- Press F2 to reset bindings to defaults.
- Saves bindings to `zumbra-nes-controls.json`.
- Removes hidden keyboard aliases from the real emulator loop.
- Removes action buffering that could leave buttons stuck after menus.
- Keeps manual Select+Start by holding the configured Select and Start keys together.

## Default player 1 bindings

- A: Z
- B: X
- Select: Tab
- Start: Enter
- Up/Down/Left/Right: arrow keys

