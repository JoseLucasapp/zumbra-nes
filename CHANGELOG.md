## 0.5.8 — Z23 Mapper 227 low-latency input hotfix

- Removed the automatic Mapper 227 idle path that starved real multicart menus.
- Replaced huge input-boost slices with short cooperative slices so SDL polling runs frequently.
- Removed the per-slice sleep while Mapper 227 is still producing the next frame.
- Extended short key taps so the ROM has enough controller-read windows to observe them.
- Documented the exact keyboard/gamepad buttons heard by the desktop frontend.

# Changelog

## 0.5.8

- Mapper 227 performance/input hotfix for the real `1200-in-1.nes` menu.
- Disabled Mapper 227 APU ticking while audio remains muted.
- Added PPU render skipping for intermediate Mapper 227 frames while preserving timing/NMI.


## 0.5.8 — Z23 responsiveness hotfix

- Added cooperative desktop emulation slices so SDL events are drained while a frame is being emulated.
- Added bounded event draining and short host yields to prevent the window manager from marking the emulator as not responding.
- Kept Mapper 227 compatibility, SRAM, save states and debugger behavior from 0.5.0.

## 0.5.0 — Z23 compatibility, persistence and debugger

- arquitetura mutável e compartilhada de mappers para CPU e PPU;
- Mapper 1/MMC1, Mapper 2/UxROM, Mapper 3/CNROM, Mapper 4/MMC3, Mapper 7/AxROM e Mapper 227;
- bank switching PRG/CHR, mirroring, PRG RAM e IRQ de MMC3;
- fórmulas de latch e proteção de CHR RAM do Mapper 227;
- SRAM de bateria persistida por SHA-256 da ROM;
- dez slots de save state com validação de schema, versão, ROM e mapper;
- snapshots de CPU, PPU, APU, bus, RAM, OAM, controles, DMA, clock e mapper;
- debugger com step, breakpoints, memória, stack, disassembly, mapper e trace;
- migração SQLite 4 e metadados de save states;
- fixture visual Mapper 0, fixture Mapper 227 e fixture de mapper incompatível;
- diagnóstico estruturado de compatibilidade e falha explícita para mappers não suportados;
- dezenove testes novos, totalizando 74;
- gate Z23 com VM/C11, desktop headless, Mapper 227, incompatibilidade, AppDir e `.deb`.

## 0.4.0 — Z22 playable emulator

- frontend SDL3 jogável para Mapper 0/NROM;
- framebuffer PPU convertido para RGBA e áudio PCM da APU enviado ao dispositivo;
- escala inteira 1×–4×, letterboxing, VSync, fullscreen e redimensionamento;
- teclado, dois gamepads, hot-plug e remapeamento dos dois jogadores;
- abertura por CLI, seletor e recentes, além de fechamento de ROM;
- pausa, reset, avanço de frame, velocidade ilimitada, FPS, volume e mute;
- SQLite para configurações, biblioteca, sessões, tempo jogado e conquistas;
- regras locais de conquistas, progresso idempotente e notificações;
- exportação/importação JSON;
- AppDir, `.deb` e caminho de AppImage via `appimagetool`;
- integração desktop escrita somente em Zumbra sobre as APIs oficiais de mídia da Zumbra 0.14.3;
- removida a ponte local `native/z22_desktop.c` e todas as declarações `extern "C"`;
- correção do latch `frameComplete` da PPU, que agora permanece ativo até ser consumido pelo scheduler;
- definição de conquistas atualizada por UPSERT e conquista de instruções movida para 100.000 instruções;
- doze testes novos, totalizando 55, e gate Z22 com VM/C11.

## 0.3.0 — Z21

- PPU Ricoh 2C02 com registradores CPU, VRAM, palette, OAM e framebuffer 256×240.
- Background, attribute tables, scroll, sprites 8×8/8×16, prioridade, flip, sprite zero hit e overflow.
- Scanlines/dots, VBlank, NMI e odd-frame skip.
- OAM DMA em `$4014` com stalls de 513/514 ciclos.
- Dois controles NES com strobe e shift serial.
- APU com pulse 1/2, triangle, noise e DMC.
- Envelopes, sweep, length/linear counters, frame sequencer, IRQs e buffer PCM.
- Scheduler integrado de CPU, PPU e APU, incluindo DMA, DMC e linhas de interrupção.
- Vinte testes de hardware adicionados, totalizando 43 arquivos de teste.
- Frontend headless atualizado com digests de frame e áudio.
- Gate Z21 com paridade VM/C11.

## 0.2.0 — Z20

- CPU Ricoh 2A03/NMOS 6502 completa no escopo de opcodes oficiais.
- 151 opcodes oficiais, modos de endereçamento, stack, vetores, IRQ/NMI e ciclos.
- Treze novos testes de CPU e 23 testes totais.
- Gate Z20 com paridade VM/C11.

## 0.1.0 — Z19

- Fundação do emulador NES/Famicom.
- iNES/NES 2.0 básico, cartucho, Mapper 0, bus, clock, fixtures e frontend headless.

## 0.4.0 — correção pré-release

### Correções de validação pré-release

- o frontend interativo não inicia mais automaticamente uma fixture sintética de teste;
- o modo headless agora executa instruções reais da CPU durante um frame completo;
- adicionada uma ROM sintética executável e determinística para smoke tests;
- adicionada regressão contra execução acidental do opcode de preenchimento `0xF4`.

