# zumbra-nes 0.5.21

Safety gate correction for Z23 stable shell validation.

## Changes

- Keeps the 0.5.20 stable shell reset behavior.
- Updates the compatibility gate to treat `zumbra project check` warning-only output as non-blocking.
- Still fails the gate when project check emits blocking semantic/type/syntax errors.
- Updates active Z23 version checks to 0.5.21.

## Validation target

The release is approved only after the full Z23 gate passes and the real desktop test opens without `field access requires a struct or enum type`.
