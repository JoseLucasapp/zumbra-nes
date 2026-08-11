# zumbra-nes 0.5.59

Z24 parser cleanup fix.

## Changes

- Fixes malformed toInt control assignments caused by the previous settings-row patch.
- Keeps drawSettingsRow receiving int values.
- Keeps Z24 menu, overlay, quick save/load and UX work.
- Keeps AppImage optional and release scripts version-driven.

## Deferred follow-ups

- Improve audio cleanup further.
- Fix D-pad/arrow behavior inside some game menus where gameplay input already works.
