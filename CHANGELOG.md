# Changelog

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
