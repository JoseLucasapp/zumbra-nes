# Z29 local achievements

Z29 keeps achievements fully offline and local-first. There is no account, no cloud sync, no leaderboard, no remote server and no hidden network dependency. Progress is stored in the local SQLite database created beside the emulator on the user's PC.

## Storage

Local achievement data lives in the regular Zumbra NES SQLite store:

- `achievement_game_metadata` registers one local achievement pack per ROM digest;
- `achievement_definitions` stores the local bundled achievement rules;
- `achievement_progress` stores current progress and unlock state;
- `achievement_events` stores local unlock history;
- `rom_library` and `play_sessions` keep the local library/session metadata.

Manual JSON export/import is only for backup, restore and debugging.

## Runtime behavior

When a ROM opens, the desktop frontend registers the ROM digest, seeds the bundled offline achievement pack and starts a local play session. During gameplay, the achievement engine evaluates frame count, controller input, session seconds, instruction count and optional memory-based rules. New unlocks are persisted immediately and shown through the desktop status/overlay path.

## Controls

- `F6` toggles the local achievements overlay;
- `F9` exports a local JSON backup to `zumbra-nes-achievements-export.json`;
- `F5` quick save also records save-state metadata in SQLite.

## Acceptance

Z29 is accepted when the full compatibility gate passes, the schema version is `5`, the project runs `83` test files, the desktop smoke still works, packages are generated and a manually launched ROM can unlock local achievements without any network dependency.
