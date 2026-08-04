# Zumbra NES 0.5.0 — Z23 compatibility, persistence and debugger

A versão 0.5.0 amplia o emulador além de NROM e adiciona persistência de estado e ferramentas de diagnóstico.

## Adicionado

- Mappers 1/MMC1, 2/UxROM, 3/CNROM, 4/MMC3, 7/AxROM e 227;
- bank switching PRG/CHR, mirroring, PRG RAM e IRQ de mapper;
- SRAM de bateria em arquivos `.sav` por SHA-256;
- dez slots de save state versionados;
- debugger com step, breakpoints, disassembly, memória, stack e trace;
- migração SQLite para metadados de save states;
- fixture visual Mapper 0;
- fixtures sintéticas Mapper 227 e mapper incompatível;
- diagnóstico claro de compatibilidade;
- dezenove testes novos, totalizando 74;
- gate Z23 com VM, C11, desktop e pacotes Linux.

## Compatibilidade

```text
0 NROM
1 MMC1/SxROM
2 UxROM
3 CNROM
4 MMC3/TxROM
7 AxROM
227 multicart
```

A lista representa famílias implementadas. Variantes de placa, submappers incomuns e ROMs dependentes de timing/opcodes não oficiais podem exigir refinamentos.

## Requisitos

- Zumbra 0.14.3;
- Linux amd64;
- SQLite e SDL3;
- nenhuma fonte C local no repositório.

## Gate

```bash
EXPECTED_ZUMBRA_VERSION=0.14.3 \
  scripts/test-z23-compatibility.sh
```
