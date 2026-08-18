# zumbra-nes 0.5.64

## Local ROM compatibility database

0.5.64 completes the local ROM compatibility milestone on top of the stable 0.5.63 Game Library baseline while keeping Zumbra-lang 0.14.5 frozen.

Highlights:

- SQLite schema 7 with one compatibility record per ROM SHA-256;
- mapper/submapper and CRC fingerprints;
- `UNTESTED`, `PLAYABLE`, `ISSUES`, `PERFECT`, `UNSUPPORTED` states;
- automatic gameplay observations without auto-claiming perfection;
- unsupported mapper records retained in the library;
- structured mapper diagnostics;
- Game Library compatibility filter;
- expanded Game Details compatibility data;
- standalone local JSON report export/import;
- non-destructive migration from 0.5.63;
- 85 direct test files plus VM/native/desktop/package release gates.

The release remains fully local-first. No account, cloud sync, server, telemetry or online compatibility database is introduced.
