#!/usr/bin/env python3
"""Generate a tiny legal NROM homebrew used to test Zumbra NES input/video.

The ROM is original test content: a small zebra-striped platformer sprite that
moves with the D-pad and jumps with A. It deliberately uses mapper 0 + CHR RAM
so it can run before the emulator supports advanced mapper features.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path

class Asm:
    def __init__(self, origin: int = 0x8000) -> None:
        self.origin = origin
        self.pc = origin
        self.code = bytearray()
        self.labels: dict[str, int] = {}
        self.refs: list[tuple[int, str, str]] = []

    def label(self, name: str) -> None:
        self.labels[name] = self.pc

    def b(self, *values: int) -> None:
        self.code.extend(v & 0xFF for v in values)
        self.pc += len(values)

    def w(self, value: int) -> None:
        self.b(value & 0xFF, (value >> 8) & 0xFF)

    def ref_abs(self, name: str) -> None:
        self.refs.append((len(self.code), name, "abs"))
        self.w(0)

    def branch(self, opcode: int, label: str) -> None:
        self.b(opcode)
        self.refs.append((len(self.code), label, "rel"))
        self.b(0)

    def lda_i(self, v): self.b(0xA9, v)
    def ldx_i(self, v): self.b(0xA2, v)
    def ldy_i(self, v): self.b(0xA0, v)
    def lda_z(self, a): self.b(0xA5, a)
    def sta_z(self, a): self.b(0x85, a)
    def stx_z(self, a): self.b(0x86, a)
    def sty_z(self, a): self.b(0x84, a)
    def lda_abs(self, a): self.b(0xAD); self.w(a)
    def sta_abs(self, a): self.b(0x8D); self.w(a)
    def stx_abs(self, a): self.b(0x8E); self.w(a)
    def sta_abs_x(self, a): self.b(0x9D); self.w(a)
    def lda_abs_x(self, a): self.b(0xBD); self.w(a)
    def txs(self): self.b(0x9A)
    def inx(self): self.b(0xE8)
    def dex(self): self.b(0xCA)
    def iny(self): self.b(0xC8)
    def tax(self): self.b(0xAA)
    def tay(self): self.b(0xA8)
    def txa(self): self.b(0x8A)
    def tya(self): self.b(0x98)
    def pha(self): self.b(0x48)
    def pla(self): self.b(0x68)
    def clc(self): self.b(0x18)
    def sec(self): self.b(0x38)
    def sei(self): self.b(0x78)
    def cld(self): self.b(0xD8)
    def rts(self): self.b(0x60)
    def rti(self): self.b(0x40)
    def nop(self): self.b(0xEA)
    def bit_abs(self, a): self.b(0x2C); self.w(a)
    def and_i(self, v): self.b(0x29, v)
    def ora_z(self, a): self.b(0x05, a)
    def cmp_i(self, v): self.b(0xC9, v)
    def cpx_i(self, v): self.b(0xE0, v)
    def adc_i(self, v): self.b(0x69, v)
    def adc_z(self, a): self.b(0x65, a)
    def sbc_i(self, v): self.b(0xE9, v)
    def jsr(self, label): self.b(0x20); self.ref_abs(label)
    def jmp(self, label): self.b(0x4C); self.ref_abs(label)
    def beq(self, label): self.branch(0xF0, label)
    def bne(self, label): self.branch(0xD0, label)
    def bpl(self, label): self.branch(0x10, label)
    def bcs(self, label): self.branch(0xB0, label)
    def bcc(self, label): self.branch(0x90, label)

    def resolve(self) -> bytes:
        for pos, name, kind in self.refs:
            if name not in self.labels:
                raise SystemExit(f"missing label: {name}")
            target = self.labels[name]
            if kind == "abs":
                self.code[pos] = target & 0xFF
                self.code[pos + 1] = (target >> 8) & 0xFF
            else:
                src = self.origin + pos + 1
                offset = target - src
                if not -128 <= offset <= 127:
                    raise SystemExit(f"branch too far to {name}: {offset}")
                self.code[pos] = offset & 0xFF
        return bytes(self.code)

def build_program() -> bytes:
    # Zero-page variables.
    PAD = 0x00
    FRAME = 0x01
    PLAYER_X = 0x02
    PLAYER_Y = 0x03
    VEL_Y = 0x04
    ON_GROUND = 0x05
    I = 0x06
    a = Asm()
    a.label("reset")
    a.sei(); a.cld(); a.ldx_i(0x40); a.stx_abs(0x4017); a.ldx_i(0xFF); a.txs(); a.inx()
    a.stx_abs(0x2000); a.stx_abs(0x2001); a.stx_abs(0x4010)
    a.bit_abs(0x2002)
    a.label("vblank1"); a.bit_abs(0x2002); a.bpl("vblank1")
    a.label("vblank2"); a.bit_abs(0x2002); a.bpl("vblank2")
    # Clear RAM pages 0-7.
    a.lda_i(0); a.tax(); a.label("clear")
    for page in range(8):
        a.sta_abs_x(page * 0x100)
    a.inx(); a.bne("clear")
    # Palette.
    a.lda_abs(0x2002); a.lda_i(0x3F); a.sta_abs(0x2006); a.lda_i(0x00); a.sta_abs(0x2006)
    a.ldx_i(0); a.label("pal_loop"); a.lda_abs_x(0)  # patch address below
    pal_ref = len(a.code) - 2
    a.sta_abs(0x2007); a.inx(); a.cpx_i(32); a.bne("pal_loop")
    # CHR RAM upload: 256 bytes.
    a.lda_abs(0x2002); a.lda_i(0x00); a.sta_abs(0x2006); a.lda_i(0x00); a.sta_abs(0x2006)
    a.ldx_i(0); a.label("chr_loop"); a.lda_abs_x(0)
    chr_ref = len(a.code) - 2
    a.sta_abs(0x2007); a.inx(); a.bne("chr_loop")
    # Hide all sprites.
    a.ldx_i(0); a.lda_i(0xFE); a.label("hide_oam"); a.sta_abs_x(0x0200); a.inx(); a.inx(); a.inx(); a.inx(); a.bne("hide_oam")
    a.lda_i(112); a.sta_z(PLAYER_X); a.lda_i(184); a.sta_z(PLAYER_Y); a.lda_i(0); a.sta_z(VEL_Y); a.lda_i(1); a.sta_z(ON_GROUND)
    a.jsr("update_sprites")
    a.lda_i(0x80); a.sta_abs(0x2000); a.lda_i(0x1E); a.sta_abs(0x2001)
    a.label("main")
    a.lda_z(FRAME); a.beq("main"); a.lda_i(0); a.sta_z(FRAME)
    a.jsr("read_pad"); a.jsr("update_player"); a.jsr("update_sprites"); a.jmp("main")

    a.label("read_pad")
    a.lda_i(1); a.sta_abs(0x4016); a.lda_i(0); a.sta_abs(0x4016); a.ldx_i(0); a.stx_z(PAD)
    a.label("pad_loop")
    a.lda_abs(0x4016); a.and_i(1); a.beq("pad_next")
    a.lda_z(PAD); a.ora_z(0x10); a.sta_z(PAD)  # overwritten below? use mask table copy not possible with OR z fixed.
    # Instead of dynamic table, unroll reads for precision.
    a.label("pad_next"); a.rts()
    # Replace read_pad with unrolled code to avoid indexed indirect features.
    start_read = a.labels["read_pad"] - a.origin
    end_read = len(a.code)
    b = Asm(a.labels["read_pad"])
    # This mini-program will overwrite the placeholder at exact size <= placeholder? Easier: rebuild separate not possible.
    # Keep placeholder unreachable by jumping to read_pad2 below.
    a.label("read_pad2")
    # not used

    # Add real read routine and change JSR later by using label read_pad_real.
    # Simpler: define it now and manually patch earlier JSR label after resolve by aliasing.
    a.labels["read_pad"] = a.pc
    a.lda_i(1); a.sta_abs(0x4016); a.lda_i(0); a.sta_abs(0x4016); a.lda_i(0); a.sta_z(PAD)
    for mask in [1,2,4,8,16,32,64,128]:
        skip = f"skip_{mask}"
        a.lda_abs(0x4016); a.and_i(1); a.beq(skip); a.lda_z(PAD); a.b(0x09, mask); a.sta_z(PAD); a.label(skip)
    a.rts()

    a.label("update_player")
    # left
    a.lda_z(PAD); a.and_i(0x40); a.beq("no_left"); a.lda_z(PLAYER_X); a.beq("no_left"); a.sec(); a.sbc_i(2); a.sta_z(PLAYER_X); a.label("no_left")
    # right
    a.lda_z(PAD); a.and_i(0x80); a.beq("no_right"); a.lda_z(PLAYER_X); a.cmp_i(232); a.bcs("no_right"); a.clc(); a.adc_i(2); a.sta_z(PLAYER_X); a.label("no_right")
    # jump with A
    a.lda_z(PAD); a.and_i(0x01); a.beq("no_jump"); a.lda_z(ON_GROUND); a.beq("no_jump"); a.lda_i(0xF4); a.sta_z(VEL_Y); a.lda_i(0); a.sta_z(ON_GROUND); a.label("no_jump")
    # gravity and floor
    a.lda_z(VEL_Y); a.clc(); a.adc_i(1); a.sta_z(VEL_Y); a.lda_z(PLAYER_Y); a.clc(); a.adc_z(VEL_Y); a.sta_z(PLAYER_Y); a.lda_z(PLAYER_Y); a.cmp_i(184); a.bcc("air"); a.lda_i(184); a.sta_z(PLAYER_Y); a.lda_i(0); a.sta_z(VEL_Y); a.lda_i(1); a.sta_z(ON_GROUND); a.label("air"); a.rts()

    a.label("update_sprites")
    # Four sprites: Y, tile, attr, X.
    # top-left
    a.lda_z(PLAYER_Y); a.sta_abs(0x0200); a.lda_i(1); a.sta_abs(0x0201); a.lda_i(0); a.sta_abs(0x0202); a.lda_z(PLAYER_X); a.sta_abs(0x0203)
    # top-right
    a.lda_z(PLAYER_Y); a.sta_abs(0x0204); a.lda_i(2); a.sta_abs(0x0205); a.lda_i(0); a.sta_abs(0x0206); a.lda_z(PLAYER_X); a.clc(); a.adc_i(8); a.sta_abs(0x0207)
    # bottom-left
    a.lda_z(PLAYER_Y); a.clc(); a.adc_i(8); a.sta_abs(0x0208); a.lda_i(3); a.sta_abs(0x0209); a.lda_i(0); a.sta_abs(0x020A); a.lda_z(PLAYER_X); a.sta_abs(0x020B)
    # bottom-right
    a.lda_z(PLAYER_Y); a.clc(); a.adc_i(8); a.sta_abs(0x020C); a.lda_i(4); a.sta_abs(0x020D); a.lda_i(0); a.sta_abs(0x020E); a.lda_z(PLAYER_X); a.clc(); a.adc_i(8); a.sta_abs(0x020F)
    a.rts()

    a.label("nmi")
    a.pha(); a.txa(); a.pha(); a.tya(); a.pha(); a.lda_i(0); a.sta_abs(0x2003); a.lda_i(2); a.sta_abs(0x4014); a.lda_i(1); a.sta_z(FRAME); a.pla(); a.tay(); a.pla(); a.tax(); a.pla(); a.rti()
    a.label("irq"); a.rti()
    a.label("palettes")
    palettes = [0x0F,0x21,0x30,0x11, 0x0F,0x16,0x27,0x30, 0x0F,0x12,0x22,0x30, 0x0F,0x00,0x10,0x20,
                0x0F,0x30,0x00,0x16, 0x0F,0x30,0x21,0x16, 0x0F,0x30,0x27,0x16, 0x0F,0x30,0x11,0x16]
    a.b(*palettes)
    a.label("chrdata")
    chr = [0]*256
    # Tile 1: face/body with black-white stripes.
    tiles = {
        1: [0b00111100,0b01111110,0b11100111,0b11011011,0b11111111,0b10100101,0b11111111,0b01111110],
        2: [0b00111100,0b01111110,0b11111111,0b10100101,0b11111111,0b11011011,0b11100111,0b01111110],
        3: [0b01111110,0b11111111,0b10100101,0b11111111,0b11011011,0b11100111,0b01111110,0b00100100],
        4: [0b01111110,0b11100111,0b11011011,0b11111111,0b10100101,0b11111111,0b01111110,0b00100100],
    }
    for tile, plane0 in tiles.items():
        off = tile*16
        for i, v in enumerate(plane0):
            chr[off+i] = v
            chr[off+8+i] = 0b01011010  # second plane creates alternating accent stripes
    a.b(*chr)
    # Patch absolute addresses for palette/chr load opcodes.
    program = bytearray(a.resolve())
    pal_addr = a.labels["palettes"]
    chr_addr = a.labels["chrdata"]
    program[pal_ref] = pal_addr & 0xFF; program[pal_ref+1] = pal_addr >> 8
    program[chr_ref] = chr_addr & 0xFF; program[chr_ref+1] = chr_addr >> 8
    # Pad and vectors for a 16 KiB NROM PRG.
    if len(program) > 0x3FFA:
        raise SystemExit(f"program too large: {len(program)}")
    program.extend([0xEA] * (0x3FFA - len(program)))
    for label in ["nmi", "reset", "irq"]:
        addr = a.labels[label]
        program.extend([addr & 0xFF, (addr >> 8) & 0xFF])
    return bytes(program)

def build_rom() -> bytes:
    header = bytearray(b"NES\x1A")
    header += bytes([1, 0, 0x00, 0x00, 0, 0, 0, 0, 0, 0, 0, 0])
    return bytes(header) + build_program()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="fixtures/homebrew/zebra-platformer.nes")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rom = build_rom()
    path = Path(args.output)
    digest = hashlib.sha256(rom).hexdigest()
    if args.check:
        if not path.exists():
            raise SystemExit(f"missing {path}")
        current = path.read_bytes()
        if current != rom:
            raise SystemExit(f"{path} is stale; regenerate it")
        print(f"zebra-platformer fixture ok: {digest}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(rom)
    print(f"wrote {path} ({len(rom)} bytes, sha256 {digest})")

if __name__ == "__main__":
    main()
