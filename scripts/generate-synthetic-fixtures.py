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



def playable_prg(size: int) -> bytearray:
    data = bytearray([0xEA] * size)
    program = bytes([
        0x78,             # SEI
        0xD8,             # CLD
        0xA2, 0xFF,       # LDX #$FF
        0x9A,             # TXS
        0xA9, 0x00,       # LDA #$00
        0x8D, 0x00, 0x20, # STA $2000
        0x8D, 0x01, 0x20, # STA $2001
        0x4C, 0x0D, 0x80, # JMP $800D
    ])
    data[0:len(program)] = program
    for vector_offset in (0x3FFA, 0x3FFC, 0x3FFE):
        target = 0x8000 if vector_offset == 0x3FFC else 0x800D
        data[vector_offset] = target & 0xFF
        data[vector_offset + 1] = (target >> 8) & 0xFF
    return data



def visible_prg(size: int) -> bytearray:
    data = bytearray([0xEA] * size)
    program = bytes([
        0x78,             # SEI
        0xD8,             # CLD
        0xA2, 0xFF,       # LDX #$FF
        0x9A,             # TXS
        0xA9, 0x00,       # LDA #$00
        0x8D, 0x00, 0x20, # STA $2000
        0x8D, 0x01, 0x20, # STA $2001
        0xA9, 0x3F,       # LDA #$3F
        0x8D, 0x06, 0x20, # STA $2006
        0xA9, 0x00,       # LDA #$00
        0x8D, 0x06, 0x20, # STA $2006
        0xA9, 0x0F,       # LDA #$0F
        0x8D, 0x07, 0x20, # STA $2007
        0xA9, 0x21,       # LDA #$21
        0x8D, 0x07, 0x20, # STA $2007
        0xA9, 0x0A,       # LDA #$0A (background + left edge)
        0x8D, 0x01, 0x20, # STA $2001
        0x4C, 0x26, 0x80, # JMP $8026
    ])
    data[0:len(program)] = program
    for vector_offset in (0x3FFA, 0x3FFC, 0x3FFE):
        target = 0x8000 if vector_offset == 0x3FFC else 0x8026
        data[vector_offset] = target & 0xFF
        data[vector_offset + 1] = (target >> 8) & 0xFF
    return data


def visible_chr() -> bytearray:
    data = bytearray(8192)
    # Tile zero: alternating vertical bars in bitplane zero.
    for row in range(8):
        data[row] = 0xAA if row % 2 == 0 else 0x55
        data[row + 8] = 0x00
    return data


def mapper227_prg() -> bytearray:
    data = bytearray(32 * 16384)
    for bank in range(32):
        start = bank * 16384
        data[start:start + 16384] = bytes([bank & 0xFF]) * 16384
    program = playable_prg(16384)
    data[0:16384] = program
    return data

def chr_data(size: int) -> bytearray:
    return bytearray((index * 7 + 1) & 0xFF for index in range(size))


files: dict[str, bytes] = {}
files["nrom-128-horizontal.nes"] = bytes(header(1, 1) + prg(16384, 0x3FFC) + chr_data(8192))
files["z22-playable-loop.nes"] = bytes(header(1, 1) + playable_prg(16384) + chr_data(8192))
files["visible-frame.nes"] = bytes(header(1, 1) + visible_prg(16384) + visible_chr())
files["mapper227-multicart.nes"] = bytes(header(32, 0, flags6=0x31, flags7=0xE0) + mapper227_prg())
files["unsupported-mapper5.nes"] = bytes(header(1, 1, flags6=0x50) + playable_prg(16384) + chr_data(8192))
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
