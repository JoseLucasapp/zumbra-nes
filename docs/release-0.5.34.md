# zumbra-nes 0.5.34 — CPU address hot-loop and desktop fast slice

This release targets the remaining frame-by-frame slowdown seen in Mapper 10 and other commercial-ROM boot screens.

## Changes

- Replaces hot-loop `AddressResult(...)` allocations with packed integer address results in `src/core/cpu6502.zum`.
- Adds `console.stepInstructionFast(...)` and `console.runFrameSliceCodeFast(...)` for the desktop performance path.
- Increases desktop instruction budgets for Mapper 10 and Mapper 227.
- Reduces renderer and runtime-memory reset frequency while preserving the reference test paths.

## Validation target

- The full Z23 gate should pass using Zumbra 0.14.4.
- Manual validation should compare Fire Emblem boot/title progression against 0.5.33.
