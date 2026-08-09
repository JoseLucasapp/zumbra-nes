# zumbra-nes 0.5.40 — smooth-frame fast PPU and Zumbra 0.14.5

This release targets the frame-by-frame/slideshow behavior seen in Fire Emblem and other Mapper 10 games.

## Main changes

- Requires Zumbra 0.14.5 with static string literal emission in the native backend.
- Removes the artificial desktop render stride that presented only some completed frames.
- Keeps fast PPU timing, but renders visible scanlines at scanline boundaries instead of doing a late full-frame snapshot.
- Keeps mapper scanline/latch events visible in the fast path to reduce lower-screen flicker.
- Keeps audio disabled in desktop performance mode until the CPU/PPU path is smooth enough to mix audio without stutter.

## Manual validation

Use Fire Emblem/Mapper 10 as the primary visual benchmark. The game should no longer look like deliberate frame skipping.
