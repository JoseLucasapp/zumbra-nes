# Arquitetura Z21

## Fluxo principal

```text
ROM → Cartridge → Mapper 0 → Bus
                         ├─ CPU 2A03
                         ├─ PPU 2C02 → framebuffer 256×240
                         ├─ APU → PCM ring buffer
                         ├─ Controller 1/2
                         └─ OAM DMA / DMC fetch
                                  ↓
                              Console scheduler
```

## Módulos de núcleo

- `header.zum`: iNES/NES 2.0;
- `cartridge.zum`: PRG, CHR, trainer e metadata;
- `mapper.zum`: Mapper 0/NROM;
- `bus.zum`: mapa CPU e roteamento PPU/APU/controles/DMA;
- `cpu6502.zum`: 151 opcodes oficiais;
- `ppu.zum`: memória, registradores, render, timing e NMI;
- `apu.zum`: canais, frame sequencer, IRQ e PCM;
- `controller.zum`: dois controles serializados;
- `console.zum`: scheduler integrado;
- `clock.zum`: relógio genérico preservado para testes históricos;
- `devices.zum`: contratos observáveis.

## Scheduler

`console.stepInstruction` executa uma instrução da CPU e avança um ciclo APU e três dots PPU para cada ciclo retornado. Depois da instrução:

- uma escrita em `$4014` dispara a cópia de 256 bytes para OAM e adiciona 513/514 ciclos;
- uma solicitação DMC busca um byte pelo CPU bus e adiciona quatro ciclos de stall;
- PPU NMI e APU IRQ são atualizadas nas fronteiras do scheduler.

## PPU

A PPU mantém estado de registradores, loopy registers `v/t/x/w`, scanline/dot, OAM, VRAM, palette e framebuffer. O render headless resolve background e sprites por pixel e produz índices de paleta estáveis.

## APU

A APU mantém os quatro geradores tradicionais mais DMC, executa quarter/half-frame clocks, gera IRQs e grava amostras unsigned de 8 bits em um ring buffer determinístico.

## Fronteiras da Z21

A Z21 é headless. Permanecem para Z22:

- janela SDL e apresentação do framebuffer;
- áudio em dispositivo real;
- teclado/gamepad real;
- seleção visual de ROM;
- save states;
- conquistas locais em SQLite.
