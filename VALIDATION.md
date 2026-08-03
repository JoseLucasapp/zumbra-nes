# Validação Z22

## Gate completo

```bash
cd ~/projects/zumbra-nes

unset Z22_SKIP_NATIVE Z22_SKIP_PACKAGES ZUMBRA_BIN
export ZUMBRA_BIN=/usr/local/bin/zumbra

EXPECTED_ZUMBRA_VERSION=0.14.3 \
  scripts/test-z22-playable.sh
```

Resultado esperado:

```text
Zumbra NES repository hygiene checks passed.
Z22 playable emulator gate passed.
```


## Código somente Zumbra

```bash
find . -path './build' -prune -o -path './dist' -prune -o -type f \( -name '*.c' -o -name '*.h' \) -print
grep -R --include='*.zum' -n 'extern "C"' src tests
```

Os dois comandos devem ficar sem saída. C gerado dentro de `build/` é detalhe interno do backend C11 e não faz parte do código-fonte da aplicação.

## Paridade VM/C11

```bash
diff -u build/vm-smoke.txt build/native-smoke.txt
```

O comando não deve imprimir diferenças.

## Smoke desktop real

Instale os requisitos de runtime disponíveis na distribuição:

```bash
sudo apt install libsqlite3-0 libsdl3-0 zenity
```

Execute com uma ROM própria Mapper 0/NROM:

```bash
./build/zumbra-nes /caminho/rom-propria.nes
```

Validar manualmente:

- janela, escala 1×–4×, redimensionamento e fullscreen;
- vídeo sem distorção e com letterboxing;
- áudio contínuo, volume e mute;
- teclado, dois gamepads e hot-plug;
- remapeamento dos dois jogadores;
- pause/reset/frame advance/fechar ROM;
- VSync, modo ilimitado e FPS;
- abertura por seletor e ROM recente;
- banco em `~/.local/share/zumbra-nes/zumbra-nes.sqlite3`;
- sessões, exportação/importação e notificações de conquista.

## Pacotes

```bash
scripts/package-z22-linux.sh
```

Verifique:

```bash
ZUMBRA_DESKTOP_HEADLESS=1 dist/zumbra-nes-0.4.0-linux-amd64.AppDir/AppRun

dpkg-deb --info dist/zumbra-nes_0.4.0_amd64.deb
dpkg-deb --contents dist/zumbra-nes_0.4.0_amd64.deb
```

Instalação real do `.deb`:

```bash
sudo apt install ./dist/zumbra-nes_0.4.0_amd64.deb
ZUMBRA_DESKTOP_HEADLESS=1 zumbra-nes
sudo apt remove zumbra-nes
```

## AppImage

Instale ou disponibilize `appimagetool` em `PATH`, `tools/appimagetool` ou `tools/appimagetool-x86_64.AppImage`, então execute novamente o script de empacotamento e valide o arquivo gerado em modo headless e visual.


## Regressão de inicialização desktop

O gate Z22 usa `fixtures/synthetic/z22-playable-loop.nes`, uma ROM sintética com loop 6502 válido e vetores definidos. O smoke desktop executa `runFrame`, não apenas os clocks de PPU/APU. Iniciar sem argumento abre o seletor de ROM e não executa automaticamente fixtures de teste.
