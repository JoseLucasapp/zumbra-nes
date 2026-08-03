#!/usr/bin/env python3
"""Verifies that metadata and decoder cover the exact official NMOS 6502 set."""
from pathlib import Path
import re
import sys

OFFICIAL = {
    int(value, 16)
    for value in """
00 01 05 06 08 09 0A 0D 0E 10 11 15 16 18 19 1D 1E
20 21 24 25 26 28 29 2A 2C 2D 2E 30 31 35 36 38 39 3D 3E
40 41 45 46 48 49 4A 4C 4D 4E 50 51 55 56 58 59 5D 5E
60 61 65 66 68 69 6A 6C 6D 6E 70 71 75 76 78 79 7D 7E
81 84 85 86 88 8A 8C 8D 8E 90 91 94 95 96 98 99 9A 9D
A0 A1 A2 A4 A5 A6 A8 A9 AA AC AD AE B0 B1 B4 B5 B6 B8 B9 BA BC BD BE
C0 C1 C4 C5 C6 C8 C9 CA CC CD CE D0 D1 D5 D6 D8 D9 DD DE
E0 E1 E4 E5 E6 E8 E9 EA EC ED EE F0 F1 F5 F6 F8 F9 FD FE
""".split()
}

root = Path(__file__).resolve().parents[1]
source = (root / "src/core/cpu6502.zum").read_text(encoding="utf-8")

metadata_region = source[source.index("pub fct opcodeInfo"):source.index("pub fct isOfficialOpcode")]
decoder_region = source[source.index("fct step(systemBus)"):]
metadata = [int(value, 16) for value in re.findall(r"case 0x([0-9A-Fa-f]{2})", metadata_region)]
decoder = [int(value, 16) for value in re.findall(r"case 0x([0-9A-Fa-f]{2})", decoder_region)]

errors = []
for name, values in (("metadata", metadata), ("decoder", decoder)):
    value_set = set(values)
    duplicates = sorted(value for value in value_set if values.count(value) > 1)
    missing = sorted(OFFICIAL - value_set)
    extra = sorted(value_set - OFFICIAL)
    if len(values) != 151:
        errors.append(f"{name}: expected 151 cases, found {len(values)}")
    if duplicates:
        errors.append(f"{name}: duplicate opcodes: {duplicates}")
    if missing:
        errors.append(f"{name}: missing opcodes: {[f'0x{x:02X}' for x in missing]}")
    if extra:
        errors.append(f"{name}: non-official opcodes: {[f'0x{x:02X}' for x in extra]}")

if errors:
    print("CPU table verification failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("CPU table verification passed: 151 metadata entries and 151 decoder cases.")
