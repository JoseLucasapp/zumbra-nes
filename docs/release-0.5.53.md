# zumbra-nes 0.5.53

Z24 visual argument type fix.

## Changes

- Fixes string numeric arguments passed to drawing helpers that expect int.
- Keeps Z24 menu, overlay, quick save/load and UX work.
- Keeps settings persisted as dict<string,string>.
- Keeps AppImage optional and release scripts version-driven.

## Deferred follow-ups

- Improve audio cleanup further.
- Fix D-pad/arrow behavior inside some game menus where gameplay input already works.
