# zumbra-nes 0.5.33 — fast desktop frame loop and Zebra Zum Adventure

This release focuses on real desktop playability instead of only passing the functional gate.

## Emulator changes

- Adds a desktop fast PPU timing mode through `console.setFastVideoTiming(...)`.
- Keeps the reference per-dot PPU path for tests and accuracy-sensitive checks.
- Renders a full framebuffer snapshot at the frame boundary with `console.renderFrameSnapshot(...)`.
- Changes the desktop loop to run toward a complete NES frame instead of advancing a few tiny slices per host frame.
- Raises the desktop slice budget and removes the artificial 10 ms cap that made real games progress in slow motion.
- Keeps runtime memory mark/reset around slices and frame rendering.
- Adds a blocking fast-frame loop gate using the legal Zebra homebrew ROM.

## Zebra homebrew changes

`fixtures/homebrew/zebra-platformer.nes` is now a larger original NROM/CHR-RAM game fixture with:

- zebra player sprite;
- jump/gravity;
- multiple platforms;
- collectible coin sprites;
- flag sprite;
- simple start/menu state;
- simple background level;
- simple APU pulse tone.

The ROM is still intentionally tiny; it is a controlled emulator fixture, not a commercial-scale game.

## Manual validation

```bash
./build/zumbra-nes --zebra
```

Controls:

```text
Setas/WASD = mover
Z/J        = pular
Esc        = sair
```

The emulator is still not cycle-perfect. The new desktop fast path is an explicit playability mode: it trades some per-dot PPU accuracy for speed while keeping the full reference implementation available for tests.
