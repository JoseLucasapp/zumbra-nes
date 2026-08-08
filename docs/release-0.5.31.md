# zumbra-nes 0.5.31 — runtime memory safety and hot-loop cleanup

This release targets the real freeze source found during Mapper 227 / multicart testing: native runtime allocations in continuous emulator hot loops.

Changes:

- removes `Mapping(...)` construction from the live CPU/PPU hot path;
- adds allocation-free mapper write/read helpers for desktop execution;
- uses the Zumbra runtime memory mark/reset API around desktop frame slices;
- adds a sustained native memory probe that runs 120 rendered frames and fails if active runtime memory keeps growing;
- keeps the legacy `Mapping` struct wrappers for tests/debugger compatibility;
- updates the Z23 compatibility gate so memory growth is now a blocking release check.

Validation:

```bash
EXPECTED_ZUMBRA_VERSION=0.14.3 scripts/test-z23-compatibility.sh
```

Expected memory check output includes:

```text
z23-memory-hotloop: ok
120
```
