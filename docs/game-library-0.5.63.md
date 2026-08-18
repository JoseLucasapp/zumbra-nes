# Game Library — 0.5.63

Zumbra NES 0.5.63 turns the existing local ROM/session/achievement database into an in-emulator library. No online account or remote service is introduced.

## Main flow

- `LOAD ROM` keeps the native picker.
- `GAME LIBRARY` opens every ROM recorded in local SQLite.
- `ACHIEVEMENTS` opens the same library pre-filtered to games with a local semantic achievement pack.
- Selecting a library entry opens `GAME DETAILS` before launching it.

## Library controls

- D-pad / keyboard Up/Down: move selection.
- D-pad / keyboard Left/Right: cycle filters.
- A or Start: open selected game.
- B or Esc: go back.
- F2: next filter.
- F3 or Select: next sort mode.
- F4: edit search text; Backspace erases, Enter finishes, Esc leaves search mode.

Filters: `ALL`, `KNOWN`, `IN PROGRESS`, `COMPLETED`, `NO PACK`.

Sort modes: `RECENT`, `TITLE`, `PROGRESS`, `PLAY TIME`, `SESSIONS`.

## Game Details

The detail view shows:

- friendly game title;
- unlocked/total achievements and completion percent;
- accumulated play time;
- session count;
- relative last-played state;
- mapper id;
- local ROM availability (`READY` / `FILE MISSING`);
- SHA-256 identity prefix.

`PLAY` launches the recorded path, `ACHIEVEMENTS` opens the per-game browser, and `BACK` returns to the library.

## Achievement browser

The browser reads the same local `achievement_definitions` and `achievement_progress` rows used by F6. Left/Right cycles `ALL`, `LOCKED`, and `UNLOCKED`. Each row shows title, description and completion/progress. F9 exports the existing local JSON backup.

## Persistence

Schema version 6 adds indexes for library title, play-time and session sorting. Existing tables and progress are preserved. New persisted timestamps use `unixTimeSeconds()`; SDL ticks remain only for monotonic runtime duration/frame pacing. Old 0.5.62 tick-based `last_opened` values are displayed as `LEGACY` until that ROM is played again.
