# zumbra-nes 0.5.33 smooth playability and release versioning

0.5.33 focuses on interactive playability after the 0.5.31/0.5.32 runtime-memory work:

- switches the desktop runtime to `console.setPerformanceMode(...)`;
- disables APU ticking in the live desktop path until the emulator reaches real-time CPU/video speed;
- advances fast PPU timing in bulk per CPU instruction instead of ticking each CPU cycle one by one;
- reduces runtime memory resets inside the hot loop;
- increases desktop CPU slice size and removes the 16 ms delay that was slowing already-behind frames;
- adds adaptive rendering stride so boot screens advance faster while still presenting regular frames;
- improves the Zebra homebrew fixture with readable in-game instructions;
- adds repository version files and tag helper scripts for Git release flow.

## Required Zumbra

This release expects Zumbra `0.14.4`.

## Git release

```bash
git add .
git commit -m "release: zumbra-nes 0.5.33 smooth playability"
git tag -a v0.5.33 -m "zumbra-nes 0.5.33"
git push origin main --tags
```
