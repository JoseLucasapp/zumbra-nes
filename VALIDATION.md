# Validação Z23

## Baseline

```text
Zumbra: 0.14.3
zumbra-nes: 0.5.0
Linux: amd64
```

## Gate completo

```bash
cd ~/projects/zumbra-nes

unset Z23_SKIP_NATIVE Z23_SKIP_PACKAGES ZUMBRA_BIN
export ZUMBRA_BIN=/usr/local/bin/zumbra

EXPECTED_ZUMBRA_VERSION=0.14.3 \
  scripts/test-z23-compatibility.sh
```

Resultado obrigatório:

```text
project test: 74 test file(s) executed
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

dpkg-deb --info dist/zumbra-nes_0.5.0_amd64.deb
dpkg-deb --contents dist/zumbra-nes_0.5.0_amd64.deb

ZUMBRA_DESKTOP_HEADLESS=1 \
  dist/zumbra-nes-0.5.0-linux-amd64.AppDir/AppRun
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
