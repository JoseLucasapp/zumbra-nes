# Mappers Z28

Z28 expands the Z23 mapper architecture while preserving its mutable mapper core, save-state snapshot model and debugger-visible mapper state.

## Registro

O registro aceita os IDs `0`, `1`, `2`, `3`, `4`, `7`, `10`, `11`, `30`, `66`, `71`, `87`, `94`, `180` e `227`. Uma ROM com outro mapper recebe um resultado estruturado de incompatibilidade antes de a máquina ser criada.

## Mapper 0 — NROM

- PRG fixo de 16 KiB espelhado ou 32 KiB;
- CHR ROM fixa ou CHR RAM;
- mirroring definido pelo header.

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

## Mapper 10 — MMC4

- PRG de 16 KiB selecionável em `$8000`;
- último banco PRG fixo em `$C000`;
- CHR de 4 KiB controlado por latches FD/FE;
- mirroring por registrador.

## Mapper 11 — Color Dreams

- banco PRG de 32 KiB selecionado pelo latch;
- banco CHR de 8 KiB selecionado pelo latch;
- mirroring vem do header.

## Mapper 30 — UNROM 512

- banco PRG de 16 KiB selecionável em `$8000`;
- último banco fixo em `$C000`;
- seleção single-screen lower/upper por bit de latch;
- CHR RAM/ROM permanece no espaço padrão.

## Mapper 66 — GxROM

- banco PRG de 32 KiB selecionável;
- banco CHR de 8 KiB selecionável;
- mirroring vem do header.

## Mapper 71 — Camerica/Codemasters

- banco PRG de 16 KiB selecionável em `$8000`;
- último banco fixo em `$C000`;
- registrador de mirroring single-screen.

## Mapper 87 — Jaleco JF-13

- PRG como NROM;
- banco CHR de 8 KiB com bits de seleção trocados.

## Mapper 94 — UN1ROM

- banco PRG de 16 KiB selecionável em `$8000` usando bits deslocados do latch;
- último banco fixo em `$C000`.

## Mapper 180 — UNROM reverse

- primeiro banco PRG fixo em `$8000`;
- banco PRG selecionável em `$C000`.

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
