# zumbra-nes 0.5.59

Z24 scope fix.

## Changes

- Fixes broken desktop.zum variable scope from the Z24 build fixes.
- Restores frames, mapperId and queuedAudioBytes declarations where needed.
- Localizes immutable parameter rewrites only inside functions that need them.
- Keeps Z24 menu, overlay, quick save/load and UX work.
- Keeps AppImage optional and release scripts version-driven.

## Deferred follow-ups

- Improve audio cleanup further.
- Fix D-pad/arrow behavior inside some game menus where gameplay input already works.
