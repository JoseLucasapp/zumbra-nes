# Zumbra NES 0.5.23

Z23 gate hardening release.

## Fixes

- Keeps `zumbra project check` advisory for the Z23 compatibility gate.
- Keeps aggregate `zumbra project test` advisory when it stops during warning-only project diagnostics.
- Adds `scripts/run-z23-tests.sh` to execute every `tests/*_test.zum` file directly.
- Preserves the existing 75-test execution requirement before VM/native/desktop/package stages.

## Approval criteria

The gate must reach:

```text
Zumbra NES Z23 compatibility
0.5.23
Project test aggregate precheck is advisory in Z23 0.5.23; running tests individually.
project test: 75 test file(s) executed
Built release desktop application: build/zumbra-nes
Z23 compatibility, persistence and debugger gate passed.
```

Warnings for unused symbols remain non-blocking for this Z23 stage.
