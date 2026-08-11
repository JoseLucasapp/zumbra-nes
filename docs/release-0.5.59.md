# zumbra-nes 0.5.59

Z24 headless desktop smoke fix.

## Changes

- Makes desktop headless smoke deterministic again.
- Validates ROM opening, then exits with the expected smoke output.
- Prevents CI/local gate from hanging after desktop build.
- Keeps Z24 menu, settings screen, overlay, quick save/load and UX work.

## Deferred follow-ups

- Reintroduce settings persistence with a typed storage wrapper.
- Improve audio cleanup further.
- Fix D-pad/arrow behavior inside some game menus where gameplay input already works.
