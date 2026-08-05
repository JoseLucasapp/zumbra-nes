# zumbra-nes 0.5.26 — desktop entrypoint return stabilization

This release fixes the Z23 desktop application pipeline after 0.5.25.

The headless native executable was already building and producing the expected Z23 smoke output, but `zumbra app doctor` and `zumbra app build` still failed with:

```text
types: function has conflicting return types: null and bool
```

## Changes

- Makes `src/desktop_main.zum` return the value from `desktop.run()` explicitly.
- Makes every early-exit branch of `desktop.run()` return `true` instead of a null return.
- Keeps startup failures non-panicking so the desktop shell can report errors safely.
- Improves the Z23 gate so app doctor output is printed before failing when the app pipeline is not ready.

## Expected gate markers

```text
Zumbra NES Z23 compatibility
0.5.26
Built release native executable: build/zumbra-nes-headless
Built release desktop application: /home/joselucasapp/projects/zumbra-nes/build/zumbra-nes
Z23 compatibility, persistence and debugger gate passed.
```
