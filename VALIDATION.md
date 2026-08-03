# Validation report — Z21 hardware 0.3.0

## Status

A Z21 integra o hardware headless do NES sobre a CPU da Z20. A aprovação oficial exige Zumbra 0.14.2, 43 testes, build C11 e saída idêntica entre VM e nativo.

## Cobertura funcional

### PPU

- oito registradores CPU com espelhamento;
- CHR ROM/RAM, nametables e palette mirrors;
- mirroring horizontal, vertical e four-screen;
- background e attribute tables;
- sprites 8×8/8×16, flip, prioridade, sprite zero hit e overflow;
- scroll, `v/t/x/w`, PPUDATA buffer e incremento 1/32;
- scanlines, dots, VBlank, NMI e odd-frame skip;
- framebuffer `256×240` e digest.

### APU

- pulse 1/2, triangle, noise e DMC;
- envelope, sweep, length/linear counters e LFSR;
- frame sequencer 4/5-step e IRQ;
- DMC address/length/loop/IRQ e fetch pelo bus;
- mixer determinístico e PCM ring buffer.

### I/O e scheduler

- dois controles serializados;
- OAM DMA com 513/514 ciclos;
- razão 3:1 PPU/CPU e 1:1 APU/CPU;
- NMI da PPU e IRQ da APU conectadas à CPU;
- paridade VM/native.

## Gate oficial

```bash
EXPECTED_ZUMBRA_VERSION=0.14.2 scripts/test-z21-hardware.sh
```

O gate executa:

1. SHA-256 das fixtures;
2. tabela/decoder dos 151 opcodes;
3. formatter e linter;
4. `project info` e versão 0.3.0;
5. análise semântica;
6. 43 testes;
7. documentação;
8. execução pela VM;
9. validação do relatório Z21;
10. build C11;
11. execução nativa;
12. comparação VM/native;
13. higiene.

## Critérios de aprovação

```text
Zumbra NES repository hygiene checks passed.
Z21 NES hardware gate passed.
```

Também devem existir:

```text
build/zumbra-nes
build/vm-run-raw.txt
build/vm-smoke.txt
build/native-smoke.txt
```

E não pode haver diferença em:

```bash
diff -u build/vm-smoke.txt build/native-smoke.txt
```
