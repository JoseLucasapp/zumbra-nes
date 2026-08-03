# Changelog

## 0.2.0 — Z20

- CPU Ricoh 2A03/NMOS 6502 completa no escopo de opcodes oficiais.
- 151 opcodes oficiais implementados e catalogados.
- Todos os modos de endereçamento oficiais.
- Registradores, flags, stack, vetores, reset, IRQ, NMI e BRK.
- Contagem de ciclos, page crossing e penalidades de branch.
- Bug de wrap da indireção do `JMP` reproduzido.
- Semântica binária de ADC/SBC mesmo com a flag decimal, como no NES.
- Integração da CPU com o bus e o scheduler da Z19.
- Treze novos testes de CPU e 23 testes totais de projeto.
- Smoke test headless executando instruções reais.
- Gate Z20 com paridade entre VM e backend C11.
- Documentação de CPU, arquitetura, testes e release 0.2.0.

## 0.1.0 — Z19

- Fundação do emulador NES/Famicom concluída.
- Parser iNES 1.0 e identificação básica NES 2.0.
- Cartucho, trainer, PRG ROM/RAM e CHR ROM/RAM.
- Mapper 0 com NROM-128 e NROM-256.
- Barramento inicial, espelhamentos e reset vector.
- Relógio determinístico CPU/PPU em razão 1:3.
- Contratos para CPU, PPU, APU, controles e frontend desktop.
- Frontend headless e persistência de metadados.
- Seis fixtures sintéticas e dez testes executáveis.
- Gate único com paridade entre VM e backend C11.
- Versão mínima atualizada para Zumbra 0.14.2, que adiciona `panic` ao backend nativo.
