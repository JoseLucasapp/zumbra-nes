# Mappers Z23

## Registro

O registro aceita os IDs `0`, `1`, `2`, `3`, `4`, `7` e `227`. Uma ROM com outro mapper recebe um resultado estruturado de incompatibilidade antes de a máquina ser criada.

## Mapper 1 — MMC1

- serialização de cinco bits;
- reset por bit 7;
- modos PRG 32 KiB, fixo inferior e fixo superior;
- CHR 8 KiB ou dois bancos de 4 KiB;
- mirroring horizontal, vertical e single-screen;
- habilitação de PRG RAM.

## Mapper 2 — UxROM

- janela selecionável de 16 KiB em `$8000`;
- último banco fixo em `$C000`;
- CHR RAM/ROM sem bank switching.

## Mapper 3 — CNROM

- PRG como NROM;
- banco CHR selecionável de 8 KiB.

## Mapper 4 — MMC3

- quatro janelas PRG de 8 KiB;
- oito janelas CHR de 1 KiB com pares de 2 KiB;
- inversão dos modos PRG/CHR;
- mirroring;
- controle de PRG RAM;
- latch, reload, enable e pending de IRQ.

O clock de IRQ é integrado ao evento de renderização por scanline do núcleo PPU atual.

## Mapper 7 — AxROM

- banco PRG de 32 KiB;
- single-screen lower/upper mirroring.

## Mapper 227

O latch é o endereço escrito em `$8000-$FFFF`. A seleção PRG usa:

```text
S = A0
p = A2-A6 + A8
L = A9
```

Os bits A7, S e L selecionam entre modo 32 KiB, 16 KiB espelhado e combinações com bancos fixos. A1 controla mirroring. Em multicarts sem bateria, A7 também protege CHR RAM nos modos NROM correspondentes.

A fixture `mapper227-multicart.nes` testa cartucho, execução e troca de bancos sem incluir conteúdo comercial.

## Compatibilidade real

O ID do mapper não descreve todas as variantes físicas. Uma ROM pode precisar de submapper, comportamento de bus conflict, RAM adicional, proteção específica ou timing de IRQ mais preciso. A tabela indica implementações disponíveis, não garantia universal para cada dump existente.
