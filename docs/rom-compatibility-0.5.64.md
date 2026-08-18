# Local ROM Compatibility Database — 0.5.64

Zumbra NES 0.5.64 keeps compatibility knowledge entirely on the user's machine. The source of truth is SQLite; JSON exists only for portable manual export/import. There is no server, account, cloud sync, telemetry or remote compatibility lookup.

## Identity

Compatibility rows are keyed by the same SHA-256 ROM digest used by the local library and achievements. Each row also records whole-image CRC-32 and content CRC-32, mapper, submapper and ROM format. SHA-256 remains the persistence identity; CRC values are diagnostic fingerprints.

## Status model

- `untested` — the ROM is recognized and its mapper is implemented, but no successful local gameplay observation has been recorded yet;
- `playable` — at least one successful local interactive session produced frames;
- `issues` — a local/imported review records known compatibility problems;
- `perfect` — reserved for an explicit local/imported review; the emulator never auto-claims perfection;
- `unsupported` — the ROM is structurally valid but its mapper is not implemented.

Automatic registration never erases a previous `perfect`, `playable` or `issues` review merely because the ROM is opened again. Automatic sessions preserve `perfect`, `issues` and `unsupported` statuses.

## Observations

A completed gameplay session records:

- video: `passed` once frames were produced;
- audio: whether audio output was enabled for the session;
- input: `passed` when player-one input was observed, otherwise `available`;
- test count;
- last-tested wall-clock timestamp;
- final observed frame.

Save support is derived from mapper support. Achievement support is derived from the bundled game-specific pack catalog.

## Unsupported ROMs

A valid ROM is registered before mapper rejection. Therefore an unsupported mapper remains visible in Game Library with its hash, mapper/submapper and diagnostic instead of disappearing after the launch error. Invalid/truncated/non-NES files are not registered as ROM compatibility rows.

## Game Library

F5 cycles an independent compatibility filter:

`ALL -> PERFECT -> PLAYABLE -> ISSUES -> UNSUPPORTED -> UNTESTED`

This combines with the existing achievement filter, search and sort controls.

Game Details shows compatibility status, mapper name, test history, video/audio/input observation, save/achievement support, known issues and ROM identity.

## Portable report

F10 writes:

`zumbra-nes-compatibility-report.json`

F11 imports the same format. The report has its own format/version marker and does not replace the existing achievement backup or save-state storage.

```json
{
  "format": "zumbra-nes-compatibility",
  "version": 1,
  "generated_at": 0,
  "records": []
}
```

Imported rows are marked with `status_source = imported`.

## Migration

Schema 7 creates `rom_compatibility` and three indexes. Existing 0.5.63 `rom_library` rows are backfilled non-destructively. Existing settings, achievements, save states, ROM history, play sessions and Game Library data are not deleted or recreated.
