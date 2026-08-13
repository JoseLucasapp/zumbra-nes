# zumbra-nes 0.5.62

Z29 local achievements offline.

## Highlights

- Keeps Zumbra-lang pinned to `0.14.5`.
- Keeps Z28 mapper compatibility and the 15 supported mapper families.
- Adds a complete local-only achievement layer backed by SQLite.
- Adds local ROM achievement metadata, unlock events, summaries and backup/export helpers.
- Adds the `F6` achievements overlay and `F9` local JSON export shortcut.
- Records quick-save metadata in SQLite when `F5` is used.
- Adds local achievement lifecycle, summary, export/import and monotonic progress tests.
- Updates the gate to schema version `5` and `83` test files.

## Out of scope

- No online accounts.
- No cloud sync.
- No leaderboard.
- No remote achievement server.
- No web dependency to unlock or view achievements.

## Gate

```text
project test: 83 test file(s) executed
Z29 local achievements, compatibility, mapper expansion, persistence and debugger gate passed.
```
