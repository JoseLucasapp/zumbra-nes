# Zumbra NES 0.1.0 — Z19

Primeira versão da fundação do emulador NES/Famicom escrita em Zumbra.

## Incluído

- iNES 1.0 e detecção NES 2.0 básica;
- Cartridge e validação de limites;
- Mapper 0/NROM-128/NROM-256;
- PRG ROM/RAM, CHR ROM/RAM e trainer;
- mapa inicial do barramento da CPU;
- reset vector;
- relógio determinístico CPU/PPU;
- contratos para devices futuros;
- frontend headless;
- metadados JSON;
- fixtures sintéticas sem ROM comercial;
- dez testes;
- gate VM e C11 nativo com comparação de saída.

## Requisito

```text
Zumbra 0.14.2
```

## Validação

```bash
EXPECTED_ZUMBRA_VERSION=0.14.2 scripts/test-z19-foundation.sh
```

## Próximo marco

Z20: implementação completa da CPU 6502.
