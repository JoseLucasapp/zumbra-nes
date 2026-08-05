# zumbra-nes 0.5.14 — Mapper 227 desktop callable bypass

This hotfix removes the remaining desktop-only helper-call indirection from the Mapper 227 command-line ROM path.

The 0.5.13 gate built the desktop executable and package artifacts, but launching the real `1200-in-1.nes` still aborted with `zumbra runtime error: value is not callable`. The failure only happened in the real SDL desktop Mapper 227 path, not in the headless compatibility smoke. Version 0.5.14 keeps the cooperative scheduler but inlines the Mapper 227 slice/present/budget decisions directly inside the main loop and presents the framebuffer directly.

## Scope

- Keeps Zumbra-lang pinned to 0.14.3.
- Keeps Mapper 227 cooperative scheduling.
- Removes unused splash/helper-call path from desktop startup.
- Updates active version checks to 0.5.14.
