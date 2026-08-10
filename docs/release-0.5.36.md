# zumbra-nes 0.5.40

Input hotfix for real ROM menus.

## Changes

- Uses SDL scancodes only in the desktop controller hot loop.
- Removes ASCII/keycode fallbacks that made `J` overlap with Start.
- Removes automatic Mapper 227 Select+Start injection after each action edge.
- Keeps manual multicart launching through Shift+Enter.
- Makes Enter/Space pure Start once a selected game is running.
