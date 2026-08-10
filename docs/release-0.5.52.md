# zumbra-nes 0.5.53

Z24 JSON settings type fix.

## Changes

- Stores Z24 audio settings as dict<string,string>.
- Stores remappable controls as dict<string,string>.
- Converts control scancodes back to int only during input polling.
- Keeps Z24 menu, overlay, quick save/load and UX work.
- Keeps AppImage optional and release scripts version-driven.

## Deferred follow-ups

- Improve audio cleanup further.
- Fix D-pad/arrow behavior inside some game menus where gameplay input already works.
