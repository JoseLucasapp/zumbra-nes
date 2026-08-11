# Z27 0.5.60 settings persistence hotfix

This overlay fixes `settings_persistence_test: volume persisted` by preserving the previous typed SQLite write path and adding safe numeric fallback only at load time.

Apply over an already patched 0.5.60 Z27 working tree, then run fmt and the full gate.
