#!/usr/bin/env python3
"""Regenerates deterministic, non-commercial NES fixtures used by Z19 tests."""
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "fixtures" / "synthetic"
OUT.mkdir(parents=True, exist_ok=True)


def header(prg_banks: int, chr_banks: int, flags6: int = 0, flags7: int = 0, byte8: int = 0, byte9: int = 0, byte10: int = 0, byte11: int = 0, byte12: int = 0) -> bytearray:
    data = bytearray(16)
    data[0:4] = b"NES\x1a"
    data[4] = prg_banks
    data[5] = chr_banks
    data[6] = flags6
    data[7] = flags7
    data[8] = byte8
    data[9] = byte9
    data[10] = byte10
    data[11] = byte11
    data[12] = byte12
    return data


def prg(size: int, reset_offset: int) -> bytearray:
    data = bytearray((index * 17 + 3) & 0xFF for index in range(size))
    data[0:4] = bytes([0xA9, 0x01, 0xEA, 0x00])
    data[reset_offset] = 0x00
    data[reset_offset + 1] = 0x80
    return data


def chr_data(size: int) -> bytearray:
    return bytearray((index * 7 + 1) & 0xFF for index in range(size))


files: dict[str, bytes] = {}
files["nrom-128-horizontal.nes"] = bytes(header(1, 1) + prg(16384, 0x3FFC) + chr_data(8192))
files["nrom-256-chr-ram.nes"] = bytes(header(2, 0, flags6=0x03) + prg(32768, 0x7FFC))
trainer = bytearray([0x5A] * 512)
files["nrom-trainer.nes"] = bytes(header(1, 1, flags6=0x04) + trainer + prg(16384, 0x3FFC) + chr_data(8192))
files["nes2-linear-header.bin"] = bytes(header(1, 1, flags7=0x08, byte8=0x20))
files["invalid-magic.bin"] = bytes(bytearray(b"BAD!" + b"\x00" * 12))
files["truncated.bin"] = b"NES\x1a\x01"

for name, content in files.items():
    (OUT / name).write_bytes(content)

with (ROOT / "fixtures" / "SHA256SUMS").open("w", encoding="utf-8") as handle:
    for name in sorted(files):
        digest = hashlib.sha256(files[name]).hexdigest()
        handle.write(f"{digest}  fixtures/synthetic/{name}\n")
