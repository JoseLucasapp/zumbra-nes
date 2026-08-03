# Validation report — Z20 CPU 6502 0.2.0

## Status

A Z20 implementa a CPU Ricoh 2A03/NMOS 6502 completa no escopo dos 151 opcodes oficiais e integra a execução ao bus da Z19.

O critério oficial exige que todo o projeto passe pela Zumbra 0.14.2 e que a saída headless seja idêntica na VM e no executável C11.

## Cobertura funcional

- 151/151 opcodes oficiais presentes na tabela e no decoder;
- 13 modos de endereçamento/variações oficiais;
- reset, IRQ, NMI e BRK;
- stack, flags e vetores;
- page crossing de loads, ALU, compares e branches;
- branch tomado/não tomado;
- bug de wrap do JMP indireto;
- semântica binária do Ricoh 2A03 para ADC/SBC;
- execução de programa sintético com loop;
- integração CPU/bus/clock/headless.

## Testes do projeto

A Z20 adiciona 13 testes de CPU aos 10 testes da Z19, totalizando 23 arquivos:

```text
cpu_reset_test.zum
cpu_addressing_test.zum
cpu_arithmetic_test.zum
cpu_decimal_mode_test.zum
cpu_shift_logic_test.zum
cpu_branch_cycle_test.zum
cpu_stack_control_test.zum
cpu_interrupt_test.zum
cpu_transfer_flags_test.zum
cpu_compare_memory_test.zum
cpu_program_test.zum
cpu_opcode_coverage_test.zum
cpu_cycle_penalty_test.zum
```

`cpu_opcode_coverage_test.zum` percorre todos os 151 opcodes oficiais e verifica que cada um permanece suportado com seus ciclos-base.

## Gate oficial

```bash
EXPECTED_ZUMBRA_VERSION=0.14.2 scripts/test-z20-cpu.sh
```

O gate executa:

1. SHA-256 das fixtures;
2. tabela e decoder com os 151 opcodes oficiais;
3. formatter em `src` e `tests`;
4. linter sem warnings;
5. `project info` e versão 0.2.0;
6. análise semântica do projeto;
7. 23 testes;
8. geração da API;
9. execução pela VM;
10. validação do relatório Z20;
11. build C11 nativo;
12. execução do binário nativo;
13. comparação exata VM/native;
14. higiene do repositório.

## Verificação rápida

```bash
Z20_SKIP_NATIVE=1 EXPECTED_ZUMBRA_VERSION=0.14.2 scripts/test-z20-cpu.sh
```

Esse modo não substitui o gate completo.

## Critérios de aprovação

```text
Zumbra NES repository hygiene checks passed.
Z20 CPU 6502 gate passed.
```

Também devem existir:

```text
build/zumbra-nes
build/vm-smoke.txt
build/native-smoke.txt
```

E o comando abaixo não deve imprimir diferenças:

```bash
diff -u build/vm-smoke.txt build/native-smoke.txt
```
