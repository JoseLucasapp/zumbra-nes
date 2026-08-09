## 0.5.43 validation — audio cleanup

- Run `EXPECTED_ZUMBRA_VERSION=0.14.5 scripts/test-z23-compatibility.sh`.
- Launch `./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"`.
- Confirm audio is cleaner, without heavy static, and input/settings/gamepad behavior remains intact.

## 0.5.43 validation — input UX

Critérios adicionais:

1. `EXPECTED_ZUMBRA_VERSION=0.14.5 scripts/test-z23-compatibility.sh` passa até gerar `build/zumbra-nes`.
2. `./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"` abre o jogo sem depender do terminal para settings.
3. `F1` mostra o overlay de controles dentro da janela.
4. `1`-`8` só remapeiam com o overlay aberto; durante gameplay normal essas teclas não entram em captura.
5. `F2` restaura o padrão com o overlay aberto.
6. Entrar em ROM/menu e soltar Enter/D-pad não deixa botão preso.
7. Controle Xbox Series S é detectado automaticamente pelo gamepad bridge, com D-pad, A/B, Select e Start.

## 0.5.43 validation

Critérios de aprovação:

1. `EXPECTED_ZUMBRA_VERSION=0.14.5 scripts/test-z23-compatibility.sh` passa até `Z23 compatibility, persistence and debugger gate passed.`
2. `./build/zumbra-nes` abre a tela `NO ROM` e permite abrir ROM por `O`/`Enter`/`Space`.
3. `./build/zumbra-nes --zebra` abre a ROM homebrew Zebra Platformer.
4. Na Zebra, setas/WASD movem o personagem e `Z`/`J` pulam.
5. `taskset -c 0 ./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"` não trava o PC e Enter/Space enviam Start+Select assistido para o menu.
6. `taskset -c 0 ./build/zumbra-nes "$HOME/Downloads/fe.nes"` não deve mais rejeitar por mapper 10; se falhar, a falha deve ser de execução/renderização, não de compatibilidade.

## 0.5.43 validation

A etapa é aprovada quando o gate completo passa, o desktop sem ROM sai da tela de logo para o shell "NO ROM", e a ROM 1200-in-1 aceita teclado no menu.

## 0.5.43 validation

A etapa bloqueante nova é o build desktop nativo. O erro `types: function has conflicting return types: null and bool` não pode aparecer.

## 0.5.23 validation

Run:

```bash
EXPECTED_ZUMBRA_VERSION=0.14.5 scripts/test-z23-compatibility.sh
./build/zumbra-nes
taskset -c 0 ./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"
```

Expected gate lines:

```text
Zumbra NES Z23 compatibility
0.5.23
Project check is advisory in Z23 0.5.23; continuing to project test/build.
Built release desktop application:
Z23 compatibility, persistence and debugger gate passed.
```

## 0.5.23 validation

Run `EXPECTED_ZUMBRA_VERSION=0.14.5 scripts/test-z23-compatibility.sh`, then `./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"`.

# Validação Z23

## Baseline

```text
Zumbra: 0.14.3
zumbra-nes: 0.5.23
Linux: amd64
```

## Gate completo

```bash
cd ~/projects/zumbra-nes

unset Z23_SKIP_NATIVE Z23_SKIP_PACKAGES ZUMBRA_BIN
export ZUMBRA_BIN=/usr/local/bin/zumbra

EXPECTED_ZUMBRA_VERSION=0.14.5 \
  scripts/test-z23-compatibility.sh
```

Resultado obrigatório:

```text
project test: 75 test file(s) executed
Zumbra NES repository hygiene checks passed.
Z23 compatibility, persistence and debugger gate passed.
```

## Smoke VM/native

```bash
cat build/vm-smoke.txt
cat build/native-smoke.txt
diff -u build/vm-smoke.txt build/native-smoke.txt
```

O `diff` deve ficar vazio.

## Desktop headless

```bash
ZUMBRA_DESKTOP_HEADLESS=1 ./build/zumbra-nes

ZUMBRA_DESKTOP_HEADLESS=1 \
  ./build/zumbra-nes fixtures/synthetic/mapper227-multicart.nes
```

Ambos devem terminar com:

```text
Z23 desktop session complete
2
```

Mapper incompatível:

```bash
ZUMBRA_DESKTOP_HEADLESS=1 \
  ./build/zumbra-nes fixtures/synthetic/unsupported-mapper5.nes

echo $?
```

O processo deve falhar e informar:

```text
ROM incompatível: mapper 5
```

## Validação visual

```bash
./build/zumbra-nes fixtures/synthetic/z23-visible-frame.nes
```

Confirmar:

- janela aberta;
- padrão visual estável;
- ausência de panic;
- pausa, reset e frame advance;
- seleção de slots `0`–`9`;
- `Q` salva e `E` restaura;
- `F` abre o debugger e `C` executa uma instrução.

## ROM Mapper 227 do usuário

A implementação é testada com uma fixture sintética Mapper 227 de 512 KiB. A ROM comercial `1200-in-1.nes` não faz parte do repositório nem da suíte automatizada. Na máquina do usuário:

```bash
./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"
```

Validar menu, seleção de bancos, mirroring e estabilidade. Falhas específicas podem indicar variante de placa, dump incorreto ou dependência de opcode não oficial.

## SRAM

Para uma ROM com battery flag:

```bash
find ~/.local/share/zumbra-nes/saves -type f -name '*.sav' -ls
```

O nome deve usar o SHA-256 da ROM. Reabrir o jogo deve restaurar a PRG RAM.

## Save states

```bash
find ~/.local/share/zumbra-nes/states -type f -name '*.zst' -ls
```

Confirmar slots diferentes e rejeição ao tentar restaurar um estado de outra ROM.

## Pacotes Linux

```bash
scripts/package-z23-linux.sh

dpkg-deb --info dist/zumbra-nes_0.5.23_amd64.deb
dpkg-deb --contents dist/zumbra-nes_0.5.23_amd64.deb

ZUMBRA_DESKTOP_HEADLESS=1 \
  dist/zumbra-nes-0.5.23-linux-amd64.AppDir/AppRun
```

AppImage é opcional e requer `appimagetool`.

## Segurança e higiene

```bash
find . \
  -path './build' -prune -o \
  -path './dist' -prune -o \
  -type f \( -name '*.c' -o -name '*.h' \) \
  -print

grep -R --include='*.zum' -n 'extern "C"' src tests
scripts/check-repository-hygiene.sh
```

Os dois primeiros comandos não devem produzir saída, e o último deve passar.


## 0.5.6 Mapper 227 input hotfix

The `1200-in-1.nes` Mapper 227 menu uses the normal NES controller polling path. The desktop frontend keeps very short key taps alive for a small host-side window and runs a temporary execution burst when input is active.


## 0.5.23 manual Mapper 227 input validation

1. Run `./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"`.
2. Click the emulator window once.
3. Press Enter/Space/keypad Enter for Start.
4. Press Right Shift/Left Shift/Tab/Backspace for Select.
5. Press arrows or WASD for menu movement.
6. Confirm inputs are processed without multi-second delay.


## 0.5.23 validation

Run:

```bash
EXPECTED_ZUMBRA_VERSION=0.14.5 scripts/test-z23-compatibility.sh
```

The `project check` and aggregate `project test` diagnostics are advisory for Z23 0.5.23. The gate must execute all 75 test files through `scripts/run-z23-tests.sh` before building native and desktop artifacts.


## 0.5.43 additional gate

The compatibility script now also runs:

```text
z23-fast-frame-loop: ok
180
```

This validates the desktop fast-timing path against the legal Zebra homebrew ROM before package creation.
