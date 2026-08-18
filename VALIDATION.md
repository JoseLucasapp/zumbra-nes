## 0.5.64 validation — local ROM compatibility database

Acceptance criteria:

1. Run `zumbra fmt --check src tests` and the release lint with Zumbra 0.14.5.
2. Run `EXPECTED_ZUMBRA_VERSION=0.14.5 scripts/test-z23-compatibility.sh` through `Zumbra NES release gate passed.`
3. Confirm `project test: 85 test file(s) executed` and SQLite schema version `7`.
4. Confirm the Game Library still lists previous 0.5.63 ROMs; existing settings, achievements, sessions, play time and save-state metadata must remain intact.
5. Open a supported ROM and verify its initial compatibility is `UNTESTED`; after a real gameplay session and return to menu it becomes `PLAYABLE` with test count/last-tested updated.
6. Verify Game Details shows mapper/name, compatibility, video/audio/input observation, save support, achievement support, known issues, test count, last tested and ROM identity.
7. Verify F5 cycles `ALL / PERFECT / PLAYABLE / ISSUES / UNSUPPORTED / UNTESTED` independently of the existing achievement filter.
8. Verify F10 exports `zumbra-nes-compatibility-report.json` and F11 imports a valid report without altering achievement/save backups.
9. Load `fixtures/synthetic/unsupported-mapper5.nes` (or another valid unsupported ROM), confirm the emulator returns to the menu instead of crashing, shows an English mapper diagnostic and persists the ROM as `UNSUPPORTED`.
10. Confirm mapper diagnostics include mapper, submapper and the supported mapper list.
11. Re-verify search/sort/achievement filters, Game Details launch, achievement browser, keyboard/gamepad navigation and Esc/B behavior.
12. Re-verify intro, audio, remap persistence, generic SDL gamepad input, F5/F8 save-state and F6 game-specific achievements.
13. Confirm AppDir and `.deb` are generated; AppImage remains optional when `appimagetool` is unavailable.
14. Confirm repository hygiene passes.

Expected final line:

```text
Zumbra NES release gate passed.
```

## 0.5.63 validation — Game Library and achievement UI

Acceptance criteria:

1. Run `zumbra fmt --check src tests` and the release lint with Zumbra 0.14.5.
2. Run `EXPECTED_ZUMBRA_VERSION=0.14.5 scripts/test-z23-compatibility.sh` through `Zumbra NES release gate passed.`
3. Confirm `project test: 84 test file(s) executed` and SQLite schema version `6`.
4. Confirm the main menu shows `GAME LIBRARY` and no development-stage/Xbox wording.
5. Open at least three previously played ROMs and verify the library lists them with play time/session/progress data.
6. Verify F2 cycles `ALL / KNOWN / IN PROGRESS / COMPLETED / NO PACK`.
7. Verify F3 cycles `RECENT / TITLE / PROGRESS / PLAY TIME / SESSIONS`.
8. Verify F4 search accepts letters/numbers/space, Backspace edits, Enter finishes and Esc leaves search without closing the library.
9. Verify keyboard and an SDL-recognized external controller can navigate rows, open details and go back consistently.
10. Open Game Details and verify ROM READY/MISSING, mapper, identity prefix, achievements, play time, sessions and last played.
11. Open the per-game achievement browser and verify ALL/LOCKED/UNLOCKED views plus descriptions/progress.
12. Confirm the main Achievements entry opens the known-games library instead of the old placeholder.
13. Confirm F9 exports the local achievement JSON from the achievement browser.
14. Launch a game from Game Details, play, return with Esc, and confirm play time/session/last-played values refresh on reopening the library.
15. Re-verify intro, audio, remap, generic gamepad input, F5/F8 save-state, F6 in-game achievements, Tetris and Popeye packs.
16. Confirm AppDir and `.deb` are generated; AppImage remains optional when `appimagetool` is unavailable.
17. Confirm repository hygiene passes.

Expected final line:

```text
Zumbra NES release gate passed.
```

## 0.5.62 validation — local achievements offline

Acceptance criteria:

1. Run `zumbra fmt` on the modified Zumbra files.
2. Run `EXPECTED_ZUMBRA_VERSION=0.14.5 scripts/test-z23-compatibility.sh` until the complete gate passes.
3. Confirm `project test: 83 test file(s) executed`.
4. Confirm schema version `5` and `mapper.supportedCount()` = `15`.
5. Confirm unsupported mapper diagnostics are in English.
6. Launch a real ROM and verify audio/input/settings/recent ROM/quick save/load still work.
7. Open Nintendo Tetris: `F6` must show 8 Tetris goals such as lines, level and score. It must not show emulator-use goals.
8. Open Nintendo Popeye: `F6` must show 8 Popeye goals based on score/round state. It must not reuse the Tetris list.
9. An unknown ROM with no bundled semantic pack must show `NO GAME-SPECIFIC PACK`; it must not fabricate frame/time/input achievements.
10. Unlock at least one supported-game achievement and confirm the toast/status shows its English name.
11. Play for at least 3 minutes and confirm audio is not bit-crushed, dragged or progressively delayed. With `F3`, `SAMPLES` should remain near one frame of 44.1 kHz audio and `QUEUE` must not grow continuously.
12. Confirm `F9` exports `zumbra-nes-achievements-export.json`; with F6 open, `E` performs the same export.
13. Confirm no login, account, online sync or achievement server exists.
14. Confirm the main menu contains no development-phase label and no Xbox-specific label.
15. Open `Controls` from the main menu, remap at least one key, press `F2` to reset, and use `Esc` to return.
16. Connect an SDL-recognized USB/Bluetooth gamepad and confirm menu/game input works without vendor-specific configuration.
17. During gameplay, press `Esc` once and confirm it returns to the emulator main menu instead of closing the application.
18. Open Controls/Achievements/About and confirm one `Esc` closes only the current overlay; `Quit` or `F12` remains the explicit exit path.
19. In Controls, press `1`, release it, then press a new letter key such as `Q`; confirm the overlay shows `Q` (not `SC`), the binding works in-game, and reopening the emulator preserves it.
20. Confirm the normal gate does not run the known-failing 119-file aggregate diagnostic precheck; it must proceed directly through the explicit `83` test files. Set `ZUMBRA_RUN_AGGREGATE_PROJECT_TEST=1` only when intentionally investigating compiler diagnostics.

Expected gate line:

```text
Zumbra NES release gate passed.
```

## 0.5.60 validation — Z27 typed settings persistence

Critérios de aprovação:

1. Rodar `zumbra fmt` nos arquivos alterados.
2. Rodar `EXPECTED_ZUMBRA_VERSION=0.14.5 scripts/test-z23-compatibility.sh` até o gate completo passar.
3. Abrir `./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"`.
4. Abrir Settings com `F1`, remapear um botão com `1`-`8`, fechar e reabrir o app.
5. Confirmar que o remap e áudio ON/OFF persistem via `zumbra-nes.sqlite3`.

## 0.5.53 validation — audio cleanup

- Run `EXPECTED_ZUMBRA_VERSION=0.14.5 scripts/test-z23-compatibility.sh`.
- Launch `./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"`.
- Confirm audio is cleaner, without heavy static, and input/settings/gamepad behavior remains intact.

## 0.5.53 validation — input UX

Critérios adicionais:

1. `EXPECTED_ZUMBRA_VERSION=0.14.5 scripts/test-z23-compatibility.sh` passa até gerar `build/zumbra-nes`.
2. `./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"` abre o jogo sem depender do terminal para settings.
3. `F1` mostra o overlay de controles dentro da janela.
4. `1`-`8` só remapeiam com o overlay aberto; durante gameplay normal essas teclas não entram em captura.
5. `F2` restaura o padrão com o overlay aberto.
6. Entrar em ROM/menu e soltar Enter/D-pad não deixa botão preso.
7. Controle Xbox Series S é detectado automaticamente pelo gamepad bridge, com D-pad, A/B, Select e Start.

## 0.5.53 validation

Critérios de aprovação:

1. `EXPECTED_ZUMBRA_VERSION=0.14.5 scripts/test-z23-compatibility.sh` passa até `Z23 compatibility, persistence and debugger gate passed.`
2. `./build/zumbra-nes` abre a tela `NO ROM` e permite abrir ROM por `O`/`Enter`/`Space`.
3. `./build/zumbra-nes --zebra` abre a ROM homebrew Zebra Platformer.
4. Na Zebra, setas/WASD movem o personagem e `Z`/`J` pulam.
5. `taskset -c 0 ./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"` não trava o PC e Enter/Space enviam Start+Select assistido para o menu.
6. `taskset -c 0 ./build/zumbra-nes "$HOME/Downloads/fe.nes"` não deve mais rejeitar por mapper 10; se falhar, a falha deve ser de execução/renderização, não de compatibilidade.

## 0.5.53 validation

A etapa é aprovada quando o gate completo passa, o desktop sem ROM sai da tela de logo para o shell "NO ROM", e a ROM 1200-in-1 aceita teclado no menu.

## 0.5.53 validation

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
./build/zumbra-nes fixtures/synthetic/visible-frame.nes
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


## 0.5.53 additional gate

The compatibility script now also runs:

```text
z23-fast-frame-loop: ok
180
```

This validates the desktop fast-timing path against the legal Zebra homebrew ROM before package creation.

## 0.5.62 final desktop polish

- F6 lifetime/numeric crash: manually confirmed fixed.
- Tetris and Popeye: manually confirmed to use different game-specific achievement packs.
- Audio: manually confirmed working after the output-boundary correction.
- Intro image: manually confirmed fitting correctly after aspect-ratio-aware scaling.
- Final checks added here: production phase labels removed from UI/runtime, Xbox-specific wording removed, Controls made functional from the main menu, external SDL Gamepad polling corrected to both 1-based slots, and Escape changed to deterministic back/menu behavior.
- Final local gate and one last controller/Controls/Escape manual pass remain required before commit/tag.
