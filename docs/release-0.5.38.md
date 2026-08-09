# zumbra-nes 0.5.40

Desktop settings compile fix.

## Changes

- Fixes the desktop app pipeline failure caused by the `data` module alias collision in `src/frontend/desktop.zum`.
- Renames JSON persistence alias to `jsondata`.
- Renames local ROM/BMP byte variables away from `data`.
- Keeps the runtime-editable controller Settings added in 0.5.40.

