# zumbra-nes 0.5.42

Audio pacing and fast-path fix.

## Changes

- Keeps fast PPU timing active when audio is enabled.
- Clocks APU in a batch fast path instead of falling back to the slow per-cycle desktop scheduler.
- Adds a low-latency audio queue guard to avoid dirty delayed buffer buildup.
- Keeps the 0.5.41 input, quit, settings and gamepad behavior.
