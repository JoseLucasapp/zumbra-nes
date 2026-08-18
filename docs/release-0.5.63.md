# zumbra-nes 0.5.63

## Scope

0.5.63 completes the Game Library and achievement UI milestone in one release. It builds directly on the 0.5.62 local-achievement SQLite model and does not change the frozen Zumbra-lang 0.14.5 baseline.

## User-facing changes

- `GAME LIBRARY` replaces the one-shot Recent ROM entry.
- Library rows show per-ROM achievement completion, play time and missing-file state.
- Filters: ALL, KNOWN, IN PROGRESS, COMPLETED, NO PACK.
- Sorts: RECENT, TITLE, PROGRESS, PLAY TIME, SESSIONS.
- F4 keyboard search with live filtering.
- Game Details exposes mapper, SHA-256 identity prefix, ROM availability, play time, sessions, last played and achievement completion.
- Achievement browser exposes ALL/LOCKED/UNLOCKED rows and descriptions.
- The main Achievements entry opens the known-games library.
- Keyboard and SDL Gamepad navigation are supported throughout the new screens.

## Persistence

SQLite schema version is 6. The migration adds query indexes only; existing ROM history, achievements, unlocks, settings and save-state metadata are preserved. Persisted wall-clock fields now use `unixTimeSeconds()` while SDL ticks remain dedicated to frame/audio/session-duration timing. Legacy 0.5.62 last-opened tick values are kept readable.

## Validation

- 84 direct `*_test.zum` files.
- New Game Library model/query regression coverage.
- Existing mapper, persistence, audio, input, save-state, achievement, native memory and fast-frame gates remain blocking.
- AppDir and `.deb` remain required release packages; AppImage is optional when `appimagetool` is unavailable.
