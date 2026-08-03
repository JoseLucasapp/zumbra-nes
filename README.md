# Zumbra NES

Emulador NES/Famicom local-first escrito em **Zumbra 0.14.3**. O repositório da aplicação contém somente código Zumbra: SDL3, vídeo, áudio, teclado e gamepads são acessados pelas APIs oficiais do runtime.

A versão `0.4.0` conclui a **Z22**: o núcleo headless das Z19–Z21 agora possui frontend desktop SDL3, vídeo e áudio reais, teclado/gamepad para dois jogadores, abertura de ROM, controles de execução, biblioteca SQLite, sessões e conquistas locais offline.

## Recursos

### Emulação

- iNES 1.0 e detecção básica NES 2.0;
- Mapper 0/NROM-128/NROM-256;
- CPU Ricoh 2A03 com 151 opcodes oficiais;
- PPU 2C02, background, sprites, scrolling, VBlank/NMI e OAM DMA;
- APU pulse 1/2, triangle, noise e DMC;
- dois controles, IRQs e scheduler CPU/PPU/APU;
- paridade determinística entre VM e backend C11;
- fronteira de frame persistente, evitando que instruções longas percam o evento de frame completo.

### Z22 desktop

- janela SDL3 redimensionável com escala inteira e letterboxing;
- framebuffer `256×240` convertido para RGBA;
- áudio mono PCM em 44,1 kHz;
- teclado, dois gamepads, hot-plug e remapeamento dos dois jogadores;
- fullscreen, VSync, escala 1×–4×, pausa, reset, fechamento/avanço de frame, mute, volume e contador de FPS;
- ROM por argumento da CLI, seletor de arquivo ou lista recente;
- suporte jogável atual limitado a Mapper 0/NROM;
- nenhuma ROM comercial incluída.

### Persistência e conquistas

O SQLite é a fonte principal para:

- configurações e remapeamento;
- biblioteca e ROMs recentes;
- sessões e tempo jogado;
- definições, progresso e desbloqueios de conquistas.

JSON é usado somente para exportação, importação e depuração.


### Código da aplicação

O `zumbra-nes` não possui arquivos `.c` ou `.h` nem declarações `extern "C"`. A aplicação chama `desktopWindowPresentRGBA`, `desktopAudioQueue`, `desktopKeyDown`, `desktopGamepadButton`, `desktopWindowSetVSync`, `processArgs`, `unixTimeSeconds` e `createFile` diretamente em Zumbra 0.14.3. O backend C11/SDL3 gerado permanece uma implementação interna do compilador/runtime, fora do código-fonte da aplicação.

## Requisitos

- Linux amd64;
- Zumbra `0.14.3`;
- Clang ou GCC;
- `libsqlite3-0`;
- `libsdl3-0` para a interface jogável;
- `zenity` recomendado para o seletor de ROM.

```bash
zumbra --version
```

Resultado esperado:

```text
0.14.3
```

## Executar

Build desktop:

```bash
zumbra app build \
  --manifest zumbra-app.toml \
  --target linux \
  --arch amd64 \
  --release \
  -o build/zumbra-nes
```

Abrir sem ROM, usando seletor/recente:

```bash
./build/zumbra-nes
```

Abrir uma ROM própria:

```bash
./build/zumbra-nes /caminho/jogo.nes
```

### Controles padrão

| Ação | Jogador 1 | Jogador 2 |
|---|---|---|
| Direcional | Setas | WASD |
| A | Z | G |
| B | X | H |
| Select | Shift direito | T |
| Start | Enter | Y |

Atalhos do emulador:

- `O`: abrir ROM;
- `P`: pausar/continuar;
- `R`: reset;
- `N`: avançar um frame;
- `M`: mute;
- `F1`: biblioteca local;
- `F2`: conquistas;
- `F3`: remapear os dois jogadores;
- `F4`: alternar velocidade ilimitada;
- `F5`: fechar a ROM atual;
- `F6` / `F7`: diminuir/aumentar escala entre 1× e 4×;
- `F8`: exportar dados locais para JSON;
- `F9`: importar o JSON exportado;
- `F10`: mostrar/ocultar FPS;
- `F11`: fullscreen;
- `F12`: alternar VSync;
- `-` / `=`: diminuir/aumentar volume;
- `Esc`: sair.

## Testes

```bash
scripts/test-z22-playable.sh
```

O gate executa:

- hashes das fixtures;
- verificação dos 151 opcodes;
- formatter e linter;
- análise do projeto;
- **55 testes**;
- documentação;
- execução VM e C11 headless;
- paridade VM/native;
- build do frontend desktop sem fontes C locais;
- smoke desktop sem display;
- AppDir e `.deb`;
- higiene do repositório.

Resultado final:

```text
Z22 playable emulator gate passed.
```

## Empacotamento Linux

```bash
scripts/package-z22-linux.sh
```

O script gera AppDir e `.deb`. AppImage também é gerado quando `appimagetool` está disponível em `PATH` ou em `tools/`.

## Estado do roadmap

- Z19 / `v0.1.0`: fundação e Mapper 0;
- Z20 / `v0.2.0`: CPU 6502;
- Z21 / `v0.3.0`: PPU, APU, controles e sincronização;
- Z22 / `v0.4.0`: frontend jogável, SQLite e conquistas locais.

A próxima etapa é a Z23: compatibilidade, novos mappers, save states e validação com ROMs homebrew/test suites legalmente redistribuíveis.
