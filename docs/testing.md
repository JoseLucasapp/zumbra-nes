# Testes da fundação

As fixtures são geradas por `scripts/generate-synthetic-fixtures.py`. Elas não contêm código ou dados de jogos comerciais.

## Testes executáveis

- `header_test.zum`: iNES 1.0;
- `nes2_header_test.zum`: NES 2.0 linear;
- `invalid_header_test.zum`: magic e tamanho inválidos;
- `cartridge_test.zum`: PRG, CHR, trainer e SHA-256;
- `mapper0_test.zum`: NROM-128/NROM-256;
- `bus_test.zum`: RAM, PPU, PRG RAM e PRG ROM;
- `chr_bus_test.zum`: CHR ROM versus CHR RAM;
- `clock_test.zum`: razão determinística 3:1;
- `headless_test.zum`: diagnóstico e reset vector;
- `metadata_test.zum`: serialização sem bytes da ROM.

## Gate

```bash
EXPECTED_ZUMBRA_VERSION=0.14.0 scripts/test-z19-foundation.sh
```

O gate valida hashes, formatação, lint, pipeline, testes, documentação, execução interpretada, compilação nativa e higiene.
