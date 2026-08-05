## 0.5.21 desktop runtime check

The real SDL command-line ROM launch must not raise `zumbra runtime error: value is not callable`.

# Testes Z23

Todas as ROMs versionadas são sintéticas e legalmente redistribuíveis.

## Total

- 55 testes herdados das Z19–Z22;
- 19 testes adicionados na Z23;
- **75 testes totais**.

## Novos grupos

### Mappers

- `mapper_registry_test.zum`;
- `mapper1_test.zum`;
- `mapper2_test.zum`;
- `mapper3_test.zum`;
- `mapper4_test.zum`;
- `mapper7_test.zum`;
- `mapper227_test.zum`;
- `mapper227_cartridge_test.zum`;
- `mapper227_execution_test.zum`;
- `mapper_compatibility_test.zum`.

### Persistência

- `save_ram_test.zum`;
- `save_state_test.zum`;
- `save_state_mismatch_test.zum`;
- `save_state_mapper_test.zum`;
- `store_save_state_test.zum`.

### Debugger

- `debugger_test.zum`;
- `debugger_breakpoint_test.zum`;
- `debugger_execution_breakpoint_test.zum`.

### Vídeo

- `visible_frame_test.zum` valida quantidade de pixels coloridos, primeiro pixel e digest do framebuffer.

## Fixtures novas

- `z23-visible-frame.nes`: Mapper 0 com paleta, CHR e nametable visíveis;
- `mapper227-multicart.nes`: 512 KiB PRG e CHR RAM;
- `unsupported-mapper5.nes`: valida o diagnóstico de incompatibilidade.

## Gate

```bash
EXPECTED_ZUMBRA_VERSION=0.14.3 \
  scripts/test-z23-compatibility.sh
```

Etapas:

1. checksums das fixtures;
2. tabela dos 151 opcodes;
3. formatter e linter;
4. versão `0.5.21`;
5. project check;
6. 75 testes pela VM;
7. documentação;
8. execução headless pela VM;
9. build/execução C11;
10. paridade VM/native;
11. app doctor e app build;
12. smoke desktop Mapper 0;
13. smoke desktop Mapper 227;
14. rejeição do Mapper 5;
15. AppDir e `.deb`;
16. higiene.

Resultado:

```text
Z23 compatibility, persistence and debugger gate passed.
```


## 0.5.6 Mapper 227 input hotfix

The `1200-in-1.nes` Mapper 227 menu uses the normal NES controller polling path. The desktop frontend keeps very short key taps alive for a small host-side window and runs a temporary execution burst when input is active.


## 0.5.21 Mapper 227 low-latency input hotfix

Manual validation target: run `./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"`, click the window once, then verify Start, Select and D-pad taps are processed without multi-second delay.

Keyboard aliases heard by player 1: Enter/Space/keypad Enter for Start, Right Shift/Left Shift/Tab/Backspace for Select, arrows/WASD for D-pad, Z/J for A, X/K for B, Esc to quit.
