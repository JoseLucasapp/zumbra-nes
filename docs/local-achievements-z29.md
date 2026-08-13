# Z29 local achievements

Z29 keeps achievements fully offline and local-first. There is no account, cloud sync, leaderboard, remote server or hidden network dependency. Progress is stored in the local SQLite database beside the emulator.

## Game identity

SHA-256 remains the canonical local persistence key for each ROM image. The cartridge loader also computes CRC-32 for the full iNES image and for PRG+CHR content. CRC aliases are used only to recognize known game revisions whose iNES headers may differ.

## Game-specific packs

Achievements describe the game, not emulator usage. The live emulator does not create goals such as `press A`, `run frames`, `CPU instructions` or `play N seconds` for commercial games.

Bundled in Z29:

- Nintendo Tetris: 8 goals based on player-one line, level and score RAM counters.
- Nintendo Popeye: 8 goals based on the six-digit score and round state.

The same supported ROM receives the same achievement definitions for every local player. Different games receive different definitions. If a ROM has no semantic pack, F6 explicitly reports `NO GAME-SPECIFIC PACK` instead of inventing meaningless goals.

A ROM hash can identify a game, but a hash cannot reveal that an arbitrary RAM address means score, level, boss state or collectibles. Supporting a new game therefore requires a small local semantic pack backed by known game state. This remains entirely offline.

## Storage

- `achievement_game_metadata`: pack metadata per ROM digest;
- `achievement_definitions`: bundled local rules;
- `achievement_progress`: monotonic progress and unlock state;
- `achievement_events`: local unlock history;
- `rom_library` and `play_sessions`: local library/session metadata.

JSON export/import is only for manual backup, restore and debugging.

## Runtime

When a ROM opens, the emulator fingerprints it, resolves a bundled pack, seeds SQLite and starts the local session. F6 reads the actual SQLite rows and shows goal, progress, `DONE`, unlocked/total and completion percentage. Unlock toasts show the English achievement name.

Achievement SQLite work remains outside the audio-critical queue path: audio is queued first, unchanged rows do not write, controller checks are edge-triggered and periodic progress checks are throttled.

## Audio boundary

The deterministic APU retains its established 40-CPU-cycle sample divider. The desktop output path converts the APU byte range into the safe input range expected by Zumbra 0.14.5's signed 16-bit SDL bridge, then uses an integer accumulator to resample the /40 stream to 44,100 Hz. This prevents int16 wrap distortion and long-term SDL queue drift without changing NES/APU timing.

F3 exposes `QUEUE` and `SAMPLES` telemetry for live audio validation.

## Controls

- `F6`: achievements overlay;
- `F9`: export local JSON backup;
- `E` while F6 is open: alternate export shortcut;
- `F3`: technical overlay including audio telemetry;
- `F5`: quick save and local save-state metadata.
