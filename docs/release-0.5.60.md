# zumbra-nes 0.5.60

Z27 typed settings persistence.

## Changes

- Reintroduces durable desktop settings through the existing SQLite settings table.
- Keeps player 1 control values as typed integers in memory.
- Persists audio muted/on-off and player 1 remaps through a typed settings wrapper.
- Stringifies values only at the SQLite settings boundary.
- Makes corrupted numeric settings fall back safely to defaults instead of crashing runtime startup.
- Adds a regression test for typed settings persistence and fallback behavior.
- Keeps the Z24 menu, overlay, quick save/load and headless smoke behavior.

## Still deferred

- Audio cleanup/static reduction.
- D-pad/arrow behavior inside some in-game menus.
