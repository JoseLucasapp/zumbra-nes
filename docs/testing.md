## 0.5.43 desktop/input/homebrew check

Comandos manuais principais:

```bash
./build/zumbra-nes
./build/zumbra-nes --zebra
taskset -c 0 ./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"
taskset -c 0 ./build/zumbra-nes "$HOME/Downloads/fe.nes"
```

A ROM `fixtures/homebrew/zebra-platformer.nes` é original do projeto e existe para testar input e renderização sem ROM comercial.

## 0.5.43 desktop intro/input check

Validar `./build/zumbra-nes` sem ROM e `taskset -c 0 ./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"`. A intro deve aparecer antes do menu da ROM, e Enter/Space/Shift/Tab/setas/WASD/Z/X/J/K devem ser capturados pela janela.

## 0.5.43 desktop app-build check

A 0.5.43 exige que `zumbra app build --manifest zumbra-app.toml --target linux --arch amd64 --release -o build/zumbra-nes` gere `build/zumbra-nes` sem `types: function has conflicting return types: null and bool`.

## 0.5.23 desktop runtime check

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
EXPECTED_ZUMBRA_VERSION=0.14.5 \
  scripts/test-z23-compatibility.sh
```

Etapas:

1. checksums das fixtures;
2. tabela dos 151 opcodes;
3. formatter e linter;
4. versão `0.5.23`;
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


## 0.5.23 Mapper 227 low-latency input hotfix

Manual validation target: run `./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"`, click the window once, then verify Start, Select and D-pad taps are processed without multi-second delay.

Keyboard aliases heard by player 1: Enter/Space/keypad Enter for Start, Right Shift/Left Shift/Tab/Backspace for Select, arrows/WASD for D-pad, Z/J for A, X/K for B, Esc to quit.

## Z23 0.5.23 test execution

`zumbra project check` and aggregate `zumbra project test` can emit unused-symbol diagnostics before executing test files. For Z23 0.5.23, the compatibility gate records those diagnostics and then runs `scripts/run-z23-tests.sh`, which executes every `tests/*_test.zum` file directly. The gate still requires `project test: 75 test file(s) executed` before native and desktop builds.


## Zebra Zum Adventure smoke

Run the original homebrew platformer fixture:

```bash
./build/zumbra-nes --zebra
```

Expected behavior: the ROM waits for Start, then the zebra can move and jump, there are visible platforms, collectible coin sprites, a flag sprite, background tiles and a simple pulse tone.
