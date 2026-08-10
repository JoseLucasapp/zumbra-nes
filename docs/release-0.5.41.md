# zumbra-nes 0.5.41

Input, menu, audio and quit behavior stabilization.

## Changes

- Esc no longer exits gameplay; it only closes/cancels Settings.
- F12 is the explicit emergency exit shortcut; window close still works.
- Input lock after ROM/settings is now fixed-duration, so holding Start/D-pad cannot freeze menus.
- Keyboard aliases restored for menus: WASD, J/K, Space, keypad Enter and Shift.
- Opposite D-pad directions are filtered before reaching the NES controller.
- Desktop audio output now drains APU samples into the runtime queue.
- Xbox-style controller polling remains automatic.
