# zumbra-nes 0.5.13 — Z23 desktop runtime callable fix

This release fixes a desktop-only runtime failure seen after the 0.5.11 gate passed and `./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"` printed:

```text
zumbra runtime error: value is not callable
```

## Changes

- Inline the startup/transition splash renderer directly inside `src/frontend/desktop.zum`.
- Remove the imported `splash.frame(...)` call from the desktop runtime path.
- Keep the cooperative Mapper 227 scheduler introduced in 0.5.11.
- Keep Zumbra-lang pinned to 0.14.3.

## Validation required on Debian

```bash
cd ~/projects/zumbra-nes
zumbra fmt src/frontend/desktop.zum src/frontend/native_bridge.zum tests/playable_headless_test.zum
EXPECTED_ZUMBRA_VERSION=0.14.3 scripts/test-z23-compatibility.sh
./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"
```

Approval criteria:

1. the gate passes to the end;
2. the desktop binary starts without `value is not callable`;
3. the Mapper 227 menu remains responsive enough for Start/Select/D-pad;
4. opening an internal game does not freeze the host window.
