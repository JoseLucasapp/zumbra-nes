# Changelog

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
- Documentação da PPU, APU, arquitetura, testes e release 0.3.0.

## 0.2.0 — Z20

- CPU Ricoh 2A03/NMOS 6502 completa no escopo de opcodes oficiais.
- 151 opcodes oficiais, modos de endereçamento, stack, vetores, IRQ/NMI e ciclos.
- Treze novos testes de CPU e 23 testes totais.
- Gate Z20 com paridade VM/C11.

## 0.1.0 — Z19

- Fundação do emulador NES/Famicom.
- iNES/NES 2.0 básico, cartucho, Mapper 0, bus, clock, fixtures e frontend headless.
