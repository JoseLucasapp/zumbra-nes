# Zumbra NES 0.3.0 — Z21 hardware

A versão 0.3.0 integra o hardware headless do NES/Famicom.

## Adicionado

- PPU 2C02, framebuffer, background, sprites, scroll, VBlank e NMI;
- APU com pulse, triangle, noise, DMC, frame sequencer e IRQs;
- controles 1/2;
- OAM DMA;
- scheduler CPU/PPU/APU;
- 20 testes de hardware;
- gate `scripts/test-z21-hardware.sh`;
- documentação de PPU/APU e arquitetura.

## Compatibilidade

- Zumbra mínima: 0.14.2;
- backend: VM e C11;
- mapper validado: Mapper 0/NROM;
- ROMs incluídas: somente fixtures sintéticas.
