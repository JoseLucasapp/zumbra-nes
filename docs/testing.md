# Testes Z20

As fixtures são geradas por `scripts/generate-synthetic-fixtures.py` e não contêm conteúdo comercial.

## Testes herdados da Z19

- `header_test.zum`: iNES 1.0;
- `nes2_header_test.zum`: NES 2.0 linear;
- `invalid_header_test.zum`: magic e tamanhos inválidos;
- `cartridge_test.zum`: PRG, CHR, trainer e SHA-256;
- `mapper0_test.zum`: NROM-128/NROM-256;
- `bus_test.zum`: RAM, PPU, PRG RAM e PRG ROM;
- `chr_bus_test.zum`: CHR ROM versus CHR RAM;
- `clock_test.zum`: razão determinística 3:1;
- `headless_test.zum`: CPU integrada ao diagnóstico;
- `metadata_test.zum`: serialização sem bytes da ROM.

## Testes de CPU adicionados na Z20

- `cpu_reset_test.zum`: estado de reset, vetor e ciclos;
- `cpu_addressing_test.zum`: modos de endereçamento e wrap de zero page;
- `cpu_arithmetic_test.zum`: ADC, SBC, lógica e flags;
- `cpu_decimal_mode_test.zum`: decimal armazenado, aritmética binária do 2A03;
- `cpu_shift_logic_test.zum`: BIT, ASL, LSR, ROL e ROR em acumulador e memória;
- `cpu_branch_cycle_test.zum`: branch tomado, não tomado e page crossing;
- `cpu_stack_control_test.zum`: stack, JSR, RTS e bug do JMP indireto;
- `cpu_interrupt_test.zum`: NMI, IRQ, BRK, RTI e bit B empilhado;
- `cpu_transfer_flags_test.zum`: transferências, incrementos e flags;
- `cpu_compare_memory_test.zum`: compares, loads/stores e INC/DEC;
- `cpu_program_test.zum`: programa sintético com loop;
- `cpu_opcode_coverage_test.zum`: 151 opcodes oficiais;
- `cpu_cycle_penalty_test.zum`: penalidades indexadas de leitura.

## Gate

```bash
EXPECTED_ZUMBRA_VERSION=0.14.2 scripts/test-z20-cpu.sh
```

O gate valida hashes, cobertura estática dos 151 opcodes, formatação, lint, pipeline, 23 testes, documentação, execução pela VM, compilação nativa, execução do binário, paridade exata VM/native e higiene.

Arquivos produzidos:

```text
build/vm-smoke.txt
build/zumbra-nes
build/native-smoke.txt
```

A aprovação nativa exige:

```bash
diff -u build/vm-smoke.txt build/native-smoke.txt
```
