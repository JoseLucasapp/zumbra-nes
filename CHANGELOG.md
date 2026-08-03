# Changelog

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

