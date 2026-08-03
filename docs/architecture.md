# Arquitetura Z19

## Camadas

### `src/core`

Código determinístico e independente de interface:

- `header.zum`: valida e interpreta iNES/NES 2.0;
- `cartridge.zum`: isola trainer, PRG e CHR;
- `mapper.zum`: contrato de mapeamento e Mapper 0;
- `bus.zum`: mapa de memória visto pela CPU;
- `clock.zum`: scheduler 3 PPU : 1 CPU;
- `devices.zum`: contratos para CPU, PPU, APU e controles.

### `src/frontend`

- `headless.zum`: diagnóstico reproduzível para testes e CI;
- `desktop_contract.zum`: estado neutro que será conectado ao SDL em marcos posteriores.

### `src/persistence`

- `metadata.zum`: grava apenas metadados e hashes. A ROM não é copiada nem armazenada.

## Fluxo

```text
arquivo .nes
    ↓
header.inspect
    ↓
cartridge.inspectImage
    ↓
Cartridge
    ↓
Mapper 0 + Bus + Clock
    ↓
frontend headless
```

## Fronteiras do Z19

O marco não interpreta opcodes, não renderiza frames e não produz áudio. Essas responsabilidades permanecem fora desta fundação:

- Z20: CPU 6502;
- Z21: PPU, APU e controles;
- Z22: execução jogável e conquistas locais.
