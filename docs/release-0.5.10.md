# Zumbra NES 0.5.10 — native hot-loop performance gate

A 0.5.10 resolves the practical Mapper 227 delay by requiring the Zumbra 0.14.3 native hot-loop compiler patch before building the emulator.

## Problem fixed

The previous frontend-only hotfixes improved event polling and input retention, but the real `1200-in-1.nes` still advanced too slowly: a button press could take tens of seconds or more to be consumed by the ROM.

## Change

This release stops treating the issue as an input mapping bug. The gate now verifies that the installed `zumbra` compiler emits optimized native C helpers for hot loops:

- inline numeric and boolean operations;
- direct array/buffer indexing;
- direct struct-field slot access;
- static string constants;
- direct function/method calls where the target is known.

If the compiler is still the older generic C backend, the gate fails before building `build/zumbra-nes` and tells the developer to install the Zumbra native hot-loop patch.

## Expected behavior

With the patched compiler installed, the Mapper 227 menu should no longer behave like one action takes tens of seconds or more. Audio for Mapper 227 remains muted until APU/timing receives a separate quality pass.
