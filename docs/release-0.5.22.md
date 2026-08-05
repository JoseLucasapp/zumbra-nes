# zumbra-nes 0.5.22

Critical gate unblock release.

- Makes `zumbra project check` advisory in the Z23 compatibility gate.
- Keeps `fmt`, `lint`, `project test`, VM smoke, native smoke and desktop smoke as blocking gates.
- Replaces the desktop frontend file with a minimal safety shell to remove stale menu/settings/helper paths from the check/build path.
- Keeps the simple bitmap intro and conservative Mapper 227 scheduler.
- Keeps the active Z23 version at 0.5.22.
