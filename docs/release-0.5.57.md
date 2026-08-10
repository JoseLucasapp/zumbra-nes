# zumbra-nes 0.5.59

Z24 safe settings baseline.

## Changes

- Stabilizes Z24 desktop settings with int controls in memory.
- Removes unstable JSON settings persistence from the desktop path for this baseline.
- Keeps menu, settings screen, overlay, quick save/load and UX work.
- Keeps AppImage optional and release scripts version-driven.

## Deferred follow-ups

- Reintroduce settings persistence with a typed storage wrapper.
- Improve audio cleanup further.
- Fix D-pad/arrow behavior inside some game menus where gameplay input already works.
