# Arquitetura Z23

## Visão geral

```text
ROM iNES/NES 2.0
        │
        ▼
    Cartridge
        │
        ▼
 Mutable Mapper Registry
  0 / 1 / 2 / 3 / 4 / 7 / 227
        │
        ▼
       Bus ─────────────── Debug breakpoints
   ┌────┼───────┬─────┐
   ▼    ▼       ▼     ▼
  CPU   PPU     APU  Controllers
   │     │       │
   │     ▼       ▼
   │ framebuffer PCM
   └──── Console scheduler
            │
   ┌────────┼───────────┐
   ▼        ▼           ▼
Desktop   Save RAM   Save states
  │                       │
  └──────── Debugger ─────┘
```

## Mapper registry

`src/core/mapper.zum` mantém um objeto mutável compartilhado pelo bus e pela PPU. Isso evita estados divergentes entre o bank switching observado pela CPU e o observado pelo renderer.

Implementações:

- Mapper 0: NROM-128/NROM-256;
- Mapper 1: shift register MMC1, modos PRG, CHR 4/8 KiB e mirroring;
- Mapper 2: banco PRG de 16 KiB com último banco fixo;
- Mapper 3: banco CHR de 8 KiB;
- Mapper 4: bancos PRG de 8 KiB, bancos CHR de 1/2 KiB, mirroring, PRG RAM e IRQ;
- Mapper 7: banco PRG de 32 KiB e one-screen mirroring;
- Mapper 227: latch pelo endereço escrito, modos 16/32 KiB, mirroring e proteção de CHR RAM.

O registro expõe `supports`, `supportedIds`, `compatibility`, `cpuRead`, `cpuWrite`, `ppuRead`, `ppuWrite`, `irqLine`, `snapshot` e `restore`.

## Bus e PPU

O bus resolve:

- RAM interna e mirrors;
- registradores PPU;
- APU/I/O;
- controles;
- OAM DMA;
- PRG RAM;
- PRG ROM pelo mapper;
- breakpoints de leitura e escrita.

A PPU usa o mesmo mapper para CHR e mirroring. O MMC3 recebe um evento filtrado de scanline durante renderização e pode elevar sua linha de IRQ.

## Persistência

### SRAM

`src/persistence/save_ram.zum` persiste somente cartuchos com battery flag. O caminho é derivado do SHA-256 da ROM, e a escrita acontece quando a PRG RAM está dirty ou no fechamento forçado.

### Save states

`src/persistence/save_state.zum` grava um snapshot binário versionado sem duplicar a PRG ROM imutável. A restauração exige igualdade de:

- schema;
- formato `Z23-0.5.0`;
- SHA-256 da ROM;
- mapper.

O frontend oferece dez slots e o SQLite registra caminho, frame e timestamp de cada slot.

## Debugger

`src/debugger/debugger.zum` trabalha sobre a máquina viva. Leituras de memória para inspeção usam `bus.peek`, que não dispara efeitos colaterais. Breakpoints de acesso são observados pelo bus; breakpoints de PC e trace são gerenciados pelo debugger.

## Desktop Pure Zumbra

O frontend continua sem código C local. Ele utiliza as APIs desktop/media oficiais da Zumbra 0.14.4 para janela, framebuffer, áudio, teclado, gamepad, diálogo e notificações.

## Limites conhecidos

A compatibilidade é definida por famílias de mapper iNES e não significa que toda variante de placa esteja certificada. Submappers, chips de expansão, timing muito específico e opcodes 6502 não oficiais podem exigir refinamento posterior. ROMs comerciais nunca são incluídas nas fixtures.
