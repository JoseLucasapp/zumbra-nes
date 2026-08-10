# zumbra-nes 0.5.59

Z24 settings row type fix.

## Changes

- Converts persisted string control values back to int before drawing settings rows.
- Fixes the desktop app doctor type error: argument 6 expects int, got string.
- Keeps Z24 menu, overlay, quick save/load and UX work.
- Keeps settings persisted as dict<string,string>.
- Keeps AppImage optional and release scripts version-driven.

## Deferred follow-ups

- Improve audio cleanup further.
- Fix D-pad/arrow behavior inside some game menus where gameplay input already works.
