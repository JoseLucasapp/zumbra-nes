# zumbra-nes 0.5.60 Z27 patch

Patch-only package with the files changed for Z27 typed settings persistence.

## Apply

From your local repository root:

```bash
cp -R /path/to/extracted/zumbra-nes-0.5.60-z27-patch/. .
export ZUMBRA_BIN="$HOME/projects/Zumbra-lang/build/zumbra"
"$ZUMBRA_BIN" fmt src/frontend/desktop.zum src/frontend/playable_headless.zum tests/playable_headless_test.zum tests/settings_persistence_test.zum src/persistence/store.zum src/frontend/settings.zum
rm -rf build nativec/build dist
EXPECTED_ZUMBRA_VERSION=0.14.5 scripts/test-z23-compatibility.sh
```

## Scope

Z27 reintroduces typed settings persistence through SQLite/store, persists audio ON/OFF and player 1 remaps, keeps controls as int in memory, and adds a regression test.
