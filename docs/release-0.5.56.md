# zumbra-nes 0.5.59

Z24 runtime control settings fix.

## Changes

- Keeps controls as int values in memory.
- Saves controls as dict<string,string> only at the JSON boundary.
- Removes dynamic toInt calls from runtime input/drawing paths.
- Avoids stale corrupted local settings during validation.
- Keeps Z24 menu, overlay, quick save/load and UX work.
- Keeps AppImage optional and release scripts version-driven.

## Deferred follow-ups

- Improve audio cleanup further.
- Fix D-pad/arrow behavior inside some game menus where gameplay input already works.
