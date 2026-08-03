# Zumbra NES 0.2.0 — Z20 CPU 6502

A versão 0.2.0 conclui a CPU do emulador NES/Famicom em Zumbra.

## Adicionado

- CPU Ricoh 2A03/NMOS 6502 em `src/core/cpu6502.zum`;
- 151 opcodes oficiais;
- tabela pública de metadata de opcodes;
- 13 modos/variações de endereçamento;
- stack, vetores e interrupções;
- contagem de ciclos e penalidades de página;
- helper de máquina sintética para testes;
- 13 testes específicos de CPU;
- gate `scripts/test-z20-cpu.sh`;
- documentação técnica completa.

## Alterado

- frontend headless agora executa `LDA #$01` e `NOP`;
- versão do projeto atualizada para 0.2.0;
- workflow passa a executar o gate Z20;
- validação e arquitetura documentam a CPU.

## Compatibilidade

- Zumbra mínima: 0.14.2;
- backend validado: VM e C11;
- mapper usado no gate: Mapper 0/NROM;
- ROMs incluídas: somente fixtures sintéticas.

## Gate

```bash
scripts/test-z20-cpu.sh
```

A release só deve ser marcada após CI verde e tag `v0.2.0` apontando para o commit aprovado.
