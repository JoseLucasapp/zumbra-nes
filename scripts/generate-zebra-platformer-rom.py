#!/usr/bin/env python3
"""Generate a legal NROM homebrew platformer used to test Zumbra NES.

The ROM is original test content: Zebra Zum Adventure, a tiny platformer fixture
with a title/menu-style background, zebra player, platforms, collectible-looking
coins, a flag and simple APU tones. It deliberately uses mapper 0 + CHR RAM so
it can run before the emulator depends on advanced mapper features.
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
    def inc_z(self, a): self.b(0xE6, a)
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
    def bmi(self, label): self.branch(0x30, label)
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
    # CHR RAM upload: 512 bytes, enough for gameplay tiles plus readable HUD/menu text.
    a.lda_abs(0x2002); a.lda_i(0x00); a.sta_abs(0x2006); a.lda_i(0x00); a.sta_abs(0x2006)
    a.ldx_i(0); a.label("chr_loop_0"); a.lda_abs_x(0)
    chr_ref = len(a.code) - 2
    a.sta_abs(0x2007); a.inx(); a.bne("chr_loop_0")
    a.ldx_i(0); a.label("chr_loop_1"); a.lda_abs_x(0)
    chr_ref_1 = len(a.code) - 2
    a.sta_abs(0x2007); a.inx(); a.bne("chr_loop_1")
    # Draw a simple level/background: top HUD line, platforms, floor, coins and flag.
    a.lda_abs(0x2002); a.lda_i(0x20); a.sta_abs(0x2006); a.lda_i(0x00); a.sta_abs(0x2006)
    a.ldx_i(0); a.label("nt_clear_0"); a.lda_i(0); a.sta_abs(0x2007); a.inx(); a.bne("nt_clear_0")
    a.ldx_i(0); a.label("nt_clear_1"); a.lda_i(0); a.sta_abs(0x2007); a.inx(); a.bne("nt_clear_1")
    a.ldx_i(0); a.label("nt_clear_2"); a.lda_i(0); a.sta_abs(0x2007); a.inx(); a.bne("nt_clear_2")
    a.ldx_i(0); a.label("nt_clear_3"); a.lda_i(0); a.sta_abs(0x2007); a.inx(); a.bne("nt_clear_3")
    # Platform 1 at row 20, columns 4..10.
    a.lda_abs(0x2002); a.lda_i(0x22); a.sta_abs(0x2006); a.lda_i(0x84); a.sta_abs(0x2006); a.ldx_i(0); a.label("plat_a"); a.lda_i(5); a.sta_abs(0x2007); a.inx(); a.cpx_i(7); a.bne("plat_a")
    # Platform 2 at row 16, columns 13..21.
    a.lda_abs(0x2002); a.lda_i(0x22); a.sta_abs(0x2006); a.lda_i(0x0D); a.sta_abs(0x2006); a.ldx_i(0); a.label("plat_b"); a.lda_i(5); a.sta_abs(0x2007); a.inx(); a.cpx_i(9); a.bne("plat_b")
    # Platform 3 at row 22, columns 23..29.
    a.lda_abs(0x2002); a.lda_i(0x22); a.sta_abs(0x2006); a.lda_i(0xD7); a.sta_abs(0x2006); a.ldx_i(0); a.label("plat_c"); a.lda_i(5); a.sta_abs(0x2007); a.inx(); a.cpx_i(7); a.bne("plat_c")
    # Floor row 26.
    a.lda_abs(0x2002); a.lda_i(0x23); a.sta_abs(0x2006); a.lda_i(0x40); a.sta_abs(0x2006); a.ldx_i(0); a.label("floor_loop"); a.lda_i(6); a.sta_abs(0x2007); a.inx(); a.cpx_i(32); a.bne("floor_loop")

    font_tiles = {
        "Z": 9, "E": 10, "B": 11, "R": 12, "A": 13, "D": 14, "S": 15, "H": 16,
        "N": 17, "T": 18, "O": 19, "W": 20, "M": 21, "V": 22, "J": 23, "U": 24,
        "P": 25, "L": 26, "F": 27, "C": 28, "I": 29, "G": 30, " ": 0, ":": 31,
    }
    def write_text(addr: int, text: str) -> None:
        a.lda_abs(0x2002); a.lda_i((addr >> 8) & 0xFF); a.sta_abs(0x2006); a.lda_i(addr & 0xFF); a.sta_abs(0x2006)
        for ch in text:
            a.lda_i(font_tiles.get(ch, 0)); a.sta_abs(0x2007)

    write_text(0x2068, "ZEBRA DASH")
    write_text(0x20CA, "ENTER START")
    write_text(0x2128, "ARROWS MOVE")
    write_text(0x216A, "Z JUMP COINS")

    # Hide all sprites.
    a.ldx_i(0); a.lda_i(0xFE); a.label("hide_oam"); a.sta_abs_x(0x0200); a.inx(); a.inx(); a.inx(); a.inx(); a.bne("hide_oam")
    a.lda_i(24); a.sta_z(PLAYER_X); a.lda_i(184); a.sta_z(PLAYER_Y); a.lda_i(0); a.sta_z(VEL_Y); a.lda_i(1); a.sta_z(ON_GROUND)
    a.lda_i(0); a.sta_z(I); a.sta_z(0x0A); a.lda_i(1); a.sta_z(0x07); a.sta_z(0x08); a.sta_z(0x09)
    # APU pulse tone so the fixture also exercises audio.
    a.lda_i(0x0F); a.sta_abs(0x4015); a.lda_i(0x30); a.sta_abs(0x4000); a.lda_i(0x80); a.sta_abs(0x4002); a.lda_i(0x02); a.sta_abs(0x4003)
    a.jsr("update_sprites")
    a.lda_i(0x80); a.sta_abs(0x2000); a.lda_i(0x1E); a.sta_abs(0x2001)
    a.label("main")
    a.lda_z(FRAME); a.beq("main"); a.lda_i(0); a.sta_z(FRAME)
    a.jsr("read_pad")
    a.lda_z(0x0A); a.beq("menu_wait")
    a.jsr("update_player"); a.jsr("update_sprites"); a.jmp("main")
    a.label("menu_wait")
    a.lda_z(PAD); a.and_i(0x08); a.beq("menu_idle")
    a.lda_i(1); a.sta_z(0x0A); a.jsr("update_sprites")
    a.label("menu_idle"); a.jmp("main")

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
    # gravity, platform snap and floor
    a.lda_z(VEL_Y); a.clc(); a.adc_i(1); a.sta_z(VEL_Y); a.lda_z(PLAYER_Y); a.clc(); a.adc_z(VEL_Y); a.sta_z(PLAYER_Y); a.lda_i(0); a.sta_z(ON_GROUND)
    # platform A: x 32..92, y 144
    a.lda_z(VEL_Y); a.bmi("plat_a_skip"); a.lda_z(PLAYER_X); a.cmp_i(32); a.bcc("plat_a_skip"); a.cmp_i(92); a.bcs("plat_a_skip"); a.lda_z(PLAYER_Y); a.cmp_i(144); a.bcc("plat_a_skip"); a.cmp_i(152); a.bcs("plat_a_skip"); a.lda_i(144); a.sta_z(PLAYER_Y); a.lda_i(0); a.sta_z(VEL_Y); a.lda_i(1); a.sta_z(ON_GROUND); a.label("plat_a_skip")
    # platform B: x 104..176, y 112
    a.lda_z(VEL_Y); a.bmi("plat_b_skip"); a.lda_z(PLAYER_X); a.cmp_i(104); a.bcc("plat_b_skip"); a.cmp_i(176); a.bcs("plat_b_skip"); a.lda_z(PLAYER_Y); a.cmp_i(112); a.bcc("plat_b_skip"); a.cmp_i(120); a.bcs("plat_b_skip"); a.lda_i(112); a.sta_z(PLAYER_Y); a.lda_i(0); a.sta_z(VEL_Y); a.lda_i(1); a.sta_z(ON_GROUND); a.label("plat_b_skip")
    # platform C: x 184..236, y 160
    a.lda_z(VEL_Y); a.bmi("plat_c_skip"); a.lda_z(PLAYER_X); a.cmp_i(184); a.bcc("plat_c_skip"); a.cmp_i(236); a.bcs("plat_c_skip"); a.lda_z(PLAYER_Y); a.cmp_i(160); a.bcc("plat_c_skip"); a.cmp_i(168); a.bcs("plat_c_skip"); a.lda_i(160); a.sta_z(PLAYER_Y); a.lda_i(0); a.sta_z(VEL_Y); a.lda_i(1); a.sta_z(ON_GROUND); a.label("plat_c_skip")
    a.lda_z(PLAYER_Y); a.cmp_i(184); a.bcc("after_floor"); a.lda_i(184); a.sta_z(PLAYER_Y); a.lda_i(0); a.sta_z(VEL_Y); a.lda_i(1); a.sta_z(ON_GROUND); a.label("after_floor")
    # Coin 1 near platform A.
    a.lda_z(0x07); a.beq("coin1_done"); a.lda_z(PLAYER_X); a.cmp_i(52); a.bcc("coin1_done"); a.cmp_i(78); a.bcs("coin1_done"); a.lda_z(PLAYER_Y); a.cmp_i(120); a.bcc("coin1_done"); a.cmp_i(152); a.bcs("coin1_done"); a.lda_i(0); a.sta_z(0x07); a.inc_z(I); a.lda_i(0x40); a.sta_abs(0x4006); a.lda_i(0x00); a.sta_abs(0x4007); a.label("coin1_done")
    # Coin 2 near platform B.
    a.lda_z(0x08); a.beq("coin2_done"); a.lda_z(PLAYER_X); a.cmp_i(140); a.bcc("coin2_done"); a.cmp_i(166); a.bcs("coin2_done"); a.lda_z(PLAYER_Y); a.cmp_i(88); a.bcc("coin2_done"); a.cmp_i(120); a.bcs("coin2_done"); a.lda_i(0); a.sta_z(0x08); a.inc_z(I); a.lda_i(0x40); a.sta_abs(0x4006); a.lda_i(0x00); a.sta_abs(0x4007); a.label("coin2_done")
    # Coin 3 near platform C.
    a.lda_z(0x09); a.beq("coin3_done"); a.lda_z(PLAYER_X); a.cmp_i(200); a.bcc("coin3_done"); a.cmp_i(226); a.bcs("coin3_done"); a.lda_z(PLAYER_Y); a.cmp_i(136); a.bcc("coin3_done"); a.cmp_i(168); a.bcs("coin3_done"); a.lda_i(0); a.sta_z(0x09); a.inc_z(I); a.lda_i(0x40); a.sta_abs(0x4006); a.lda_i(0x00); a.sta_abs(0x4007); a.label("coin3_done")
    a.rts()

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
    # Three collectible coins and a flag.
    a.lda_z(0x07); a.beq("hide_coin1"); a.lda_i(128); a.sta_abs(0x0210); a.lda_i(7); a.sta_abs(0x0211); a.lda_i(1); a.sta_abs(0x0212); a.lda_i(64); a.sta_abs(0x0213); a.jmp("coin1_sprite_done"); a.label("hide_coin1"); a.lda_i(0xFE); a.sta_abs(0x0210); a.label("coin1_sprite_done")
    a.lda_z(0x08); a.beq("hide_coin2"); a.lda_i(96); a.sta_abs(0x0214); a.lda_i(7); a.sta_abs(0x0215); a.lda_i(1); a.sta_abs(0x0216); a.lda_i(152); a.sta_abs(0x0217); a.jmp("coin2_sprite_done"); a.label("hide_coin2"); a.lda_i(0xFE); a.sta_abs(0x0214); a.label("coin2_sprite_done")
    a.lda_z(0x09); a.beq("hide_coin3"); a.lda_i(144); a.sta_abs(0x0218); a.lda_i(7); a.sta_abs(0x0219); a.lda_i(1); a.sta_abs(0x021A); a.lda_i(212); a.sta_abs(0x021B); a.jmp("coin3_sprite_done"); a.label("hide_coin3"); a.lda_i(0xFE); a.sta_abs(0x0218); a.label("coin3_sprite_done")
    a.lda_i(176); a.sta_abs(0x021C); a.lda_i(8); a.sta_abs(0x021D); a.lda_i(2); a.sta_abs(0x021E); a.lda_i(240); a.sta_abs(0x021F)
    a.rts()

    a.label("nmi")
    a.pha(); a.txa(); a.pha(); a.tya(); a.pha(); a.lda_i(0); a.sta_abs(0x2003); a.lda_i(2); a.sta_abs(0x4014); a.lda_i(1); a.sta_z(FRAME); a.pla(); a.tay(); a.pla(); a.tax(); a.pla(); a.rti()
    a.label("irq"); a.rti()
    a.label("palettes")
    palettes = [0x0F,0x21,0x30,0x11, 0x0F,0x16,0x27,0x30, 0x0F,0x12,0x22,0x30, 0x0F,0x00,0x10,0x20,
                0x0F,0x30,0x00,0x16, 0x0F,0x30,0x21,0x16, 0x0F,0x30,0x27,0x16, 0x0F,0x30,0x11,0x16]
    a.b(*palettes)
    a.label("chrdata")
    chr = [0]*512
    # Tiles 1-4: zebra body. 5: platform. 6: ground. 7: coin. 8: flag.
    tiles = {
        1: [0b00111100,0b01111110,0b11100111,0b11011011,0b11111111,0b10100101,0b11111111,0b01111110],
        2: [0b00111100,0b01111110,0b11111111,0b10100101,0b11111111,0b11011011,0b11100111,0b01111110],
        3: [0b01111110,0b11111111,0b10100101,0b11111111,0b11011011,0b11100111,0b01111110,0b00100100],
        4: [0b01111110,0b11100111,0b11011011,0b11111111,0b10100101,0b11111111,0b01111110,0b00100100],
        5: [0b11111111,0b11000011,0b10111101,0b10100101,0b10111101,0b11000011,0b11111111,0b11111111],
        6: [0b11111111,0b10000001,0b10111101,0b10100101,0b10100101,0b10111101,0b10000001,0b11111111],
        7: [0b00011000,0b00111100,0b01111110,0b01111110,0b01111110,0b01111110,0b00111100,0b00011000],
        8: [0b00010000,0b00110000,0b01111110,0b01111110,0b00110000,0b00010000,0b00010000,0b00010000],
    }
    glyphs = {
        9:  [0b11111110,0b00001100,0b00011000,0b00110000,0b01100000,0b11000000,0b11111110,0], # Z
        10: [0b11111110,0b11000000,0b11111000,0b11000000,0b11000000,0b11000000,0b11111110,0], # E
        11: [0b11111000,0b11001100,0b11001100,0b11111000,0b11001100,0b11001100,0b11111000,0], # B
        12: [0b11111000,0b11001100,0b11001100,0b11111000,0b11011000,0b11001100,0b11000110,0], # R
        13: [0b00111000,0b01101100,0b11000110,0b11111110,0b11000110,0b11000110,0b11000110,0], # A
        14: [0b11111000,0b11001100,0b11000110,0b11000110,0b11000110,0b11001100,0b11111000,0], # D
        15: [0b01111100,0b11000000,0b11000000,0b01111000,0b00001100,0b00001100,0b11111000,0], # S
        16: [0b11000110,0b11000110,0b11000110,0b11111110,0b11000110,0b11000110,0b11000110,0], # H
        17: [0b11000110,0b11100110,0b11110110,0b11011110,0b11001110,0b11000110,0b11000110,0], # N
        18: [0b11111110,0b00110000,0b00110000,0b00110000,0b00110000,0b00110000,0b00110000,0], # T
        19: [0b01111100,0b11000110,0b11000110,0b11000110,0b11000110,0b11000110,0b01111100,0], # O
        20: [0b11000110,0b11000110,0b11010110,0b11010110,0b11111110,0b11101110,0b11000110,0], # W
        21: [0b11000110,0b11101110,0b11111110,0b11010110,0b11000110,0b11000110,0b11000110,0], # M
        22: [0b11000110,0b11000110,0b11000110,0b01101100,0b01101100,0b00111000,0b00111000,0], # V
        23: [0b00011110,0b00001100,0b00001100,0b00001100,0b11001100,0b11001100,0b01111000,0], # J
        24: [0b11000110,0b11000110,0b11000110,0b11000110,0b11000110,0b11000110,0b01111100,0], # U
        25: [0b11111000,0b11001100,0b11001100,0b11111000,0b11000000,0b11000000,0b11000000,0], # P
        26: [0b11000000,0b11000000,0b11000000,0b11000000,0b11000000,0b11000000,0b11111110,0], # L
        27: [0b11111110,0b11000000,0b11000000,0b11111000,0b11000000,0b11000000,0b11000000,0], # F
        28: [0b01111100,0b11000110,0b11000000,0b11000000,0b11000000,0b11000110,0b01111100,0], # C
        29: [0b01111100,0b00110000,0b00110000,0b00110000,0b00110000,0b00110000,0b01111100,0], # I
        30: [0b01111100,0b11000110,0b11000000,0b11011110,0b11000110,0b11000110,0b01111100,0], # G
        31: [0b00000000,0b00110000,0b00110000,0b00000000,0b00110000,0b00110000,0b00000000,0], # :
    }
    for tile, plane0 in tiles.items():
        off = tile*16
        for i, v in enumerate(plane0):
            chr[off+i] = v
            chr[off+8+i] = 0b01011010  # second plane creates alternating accent stripes
    for tile, plane0 in glyphs.items():
        off = tile*16
        for i, v in enumerate(plane0):
            chr[off+i] = v
            chr[off+8+i] = 0
    a.b(*chr)
    # Patch absolute addresses for palette/chr load opcodes.
    program = bytearray(a.resolve())
    pal_addr = a.labels["palettes"]
    chr_addr = a.labels["chrdata"]
    program[pal_ref] = pal_addr & 0xFF; program[pal_ref+1] = pal_addr >> 8
    program[chr_ref] = chr_addr & 0xFF; program[chr_ref+1] = chr_addr >> 8
    program[chr_ref_1] = (chr_addr + 256) & 0xFF; program[chr_ref_1+1] = (chr_addr + 256) >> 8
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
