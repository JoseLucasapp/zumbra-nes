# Zumbra NES 0.5.16 — native method hot-loop requirement

A 0.5.16 is the first Z23 patch that treats the 1200-in-1 slowdown/freeze as a runtime allocation problem in native method dispatch, not as an input bug.

The emulator must be built with the Zumbra 0.14.3 native method hot-loop compiler patch. That compiler avoids materializing bound method values on every CPU/PPU hot-loop method call, which prevents unbounded allocation and host freezes while Mapper 227 ROMs are running.

This release keeps the conservative Mapper 227 cooperative scheduler and adds a stronger compiler marker check before the gate builds the desktop app.

Validation target:

```bash
EXPECTED_ZUMBRA_VERSION=0.14.3 scripts/test-z23-compatibility.sh
./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"
```

Expected behavior: menu remains responsive, Esc closes quickly, and selecting a game must not hang or get killed by the host.
