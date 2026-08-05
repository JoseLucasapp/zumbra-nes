# zumbra-nes 0.5.15 — Mapper 227 OOM guard and reusable framebuffer

The 0.5.14 gate built correctly and the real desktop binary launched, but `1200-in-1.nes` was still slow in the menu and the process was killed after an internal game switched to a prolonged black screen.

This release focuses on desktop safety and allocation pressure:

- reuses one RGBA buffer per loaded game instead of allocating a new 256x240x4 buffer on every present;
- adds `palette.rgbaBuffer` and `palette.writeRgba` while keeping the existing `palette.rgba` API for tests/headless paths;
- adds `console.runFrameSliceCode` so the desktop hot loop avoids allocating a dictionary for every mapper 227 micro-slice;
- keeps the mapper 227 event loop cooperative even when the faster/unlimited command is toggled;
- skips achievement evaluation for mapper 227 multicart frames, avoiding per-frame allocation in the heavy path;
- skips presenting prolonged black/uniform frames once a visible frame has already appeared;
- pauses mapper 227 after a long black-screen run instead of letting it consume the desktop until the OS kills the process;
- shows a lightweight startup intro before the ROM starts.

`fe.nes` still fails by design when it uses mapper 10; mapper 10 is not part of Z23 support.
