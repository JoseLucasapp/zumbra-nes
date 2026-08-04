# Zumbra NES

Emulador NES/Famicom local-first escrito em **Zumbra 0.14.3**. O repositório da aplicação contém somente código `.zum`; vídeo, áudio, teclado, gamepads e integração desktop são fornecidos pelas APIs oficiais do runtime Zumbra.

A versão **0.5.8** corrige a latência de input do Mapper 227 na ROM real `1200-in-1.nes` com fatias cooperativas e sem idle agressivo. A versão **0.5.0** concluiu a **Z23**: adiciona uma arquitetura mutável de mappers, suporte aos mappers 1, 2, 3, 4, 7 e 227, SRAM persistente, dez slots de save state, debugger, fixture visual e diagnósticos explícitos de compatibilidade.

## Compatibilidade

Mappers implementados:

- `0` — NROM;
- `1` — MMC1/SxROM;
- `2` — UxROM;
- `3` — CNROM;
- `4` — MMC3/TxROM;
- `7` — AxROM;
- `227` — multicarts baseadas em latch de endereço.

A implementação cobre os comportamentos iNES usuais dessas famílias. Variantes específicas de placa, submappers incomuns, chips adicionais e ROMs que dependem de opcodes 6502 não oficiais ainda podem exigir trabalho adicional. Nenhuma ROM comercial é incluída.

## Recursos

### Núcleo

- iNES 1.0 e detecção básica NES 2.0;
- CPU Ricoh 2A03 com os 151 opcodes oficiais;
- PPU 2C02 com background, sprites, scrolling, VBlank/NMI e OAM DMA;
- APU com pulse 1/2, triangle, noise e DMC;
- dois controles e scheduler CPU/PPU/APU;
- bank switching PRG/CHR e mirroring controlado pelo mapper;
- IRQ de MMC3 integrado à linha de IRQ da CPU;
- CHR RAM e proteção de escrita do Mapper 227;
- paridade determinística entre VM e backend C11.

### Persistência

SQLite continua sendo a fonte principal para:

- configurações e remapeamento;
- biblioteca e ROMs recentes;
- sessões e tempo jogado;
- conquistas locais;
- metadados de save states.

A Z23 adiciona:

- SRAM de bateria em `saves/<sha256>.sav`;
- flush por dirty flag e no fechamento da sessão;
- save states portáveis em `states/<sha256>-slotN.zst`;
- dez slots, de `0` a `9`;
- validação de schema, versão, SHA-256 da ROM e mapper antes da restauração;
- serialização de CPU, PPU, APU, bus, RAM, OAM, controles, DMA, relógio e mapper.

JSON permanece restrito a exportação, importação e depuração.

### Debugger

O debugger Z23 oferece:

- pausa e retomada;
- step de instrução e step de frame;
- breakpoints de PC;
- breakpoints de leitura e escrita no bus;
- leitura de registradores, flags, stack e memória;
- disassembly baseado na tabela oficial de opcodes;
- inspeção do mapper;
- trace limitado;
- painel desktop de diagnóstico.

### Desktop

- janela SDL3 redimensionável;
- framebuffer `256×240` em RGBA;
- áudio PCM mono a 44,1 kHz;
- teclado e dois gamepads;
- fullscreen, VSync, escala 1×–4× e letterboxing;
- abertura por CLI, seletor e lista recente;
- pausa, reset, avanço de frame, mute, volume e FPS;
- mensagens claras para mappers não suportados;
- nenhuma fonte `.c` ou `.h` mantida no repositório.

## Requisitos

- Linux amd64;
- Zumbra `0.14.3`;
- Clang ou GCC;
- `libsqlite3-0`;
- `libsdl3-0` para a interface gráfica;
- `zenity` recomendado para o seletor de ROM;
- `appimagetool` opcional para AppImage.

```bash
zumbra --version
```

Resultado esperado:

```text
0.14.3
```

## Build e execução

```bash
zumbra app build \
  --manifest zumbra-app.toml \
  --target linux \
  --arch amd64 \
  --release \
  -o build/zumbra-nes
```

Abrir o seletor:

```bash
./build/zumbra-nes
```

Abrir uma ROM própria:

```bash
./build/zumbra-nes /caminho/jogo.nes
```

Fixture visual legalmente redistribuível:

```bash
./build/zumbra-nes fixtures/synthetic/z23-visible-frame.nes
```

Fixture sintética Mapper 227:

```bash
./build/zumbra-nes fixtures/synthetic/mapper227-multicart.nes
```

## Controles

| Ação | Jogador 1 | Jogador 2 |
|---|---|---|
| Direcional | Setas | WASD |
| A | Z | G |
| B | X | H |
| Select | Shift direito | T |
| Start | Enter | Y |

Atalhos:

- `O`: abrir ROM;
- `P`: pausar/continuar;
- `R`: reset;
- `N`: avançar um frame;
- `M`: mute;
- `F1`: biblioteca;
- `F2`: conquistas;
- `F3`: remapear controles;
- `F4`: velocidade ilimitada;
- `F5`: fechar ROM;
- `F6` / `F7`: escala;
- `F8` / `F9`: exportar/importar JSON;
- `F10`: FPS;
- `F11`: fullscreen;
- `F12`: VSync;
- `0`–`9`: selecionar slot de save state;
- `Q`: salvar no slot selecionado;
- `E`: carregar o slot selecionado;
- `F`: abrir o painel do debugger;
- `C`: executar uma instrução quando pausado;
- `-` / `=`: volume;
- `Esc`: sair.

## Testes

```bash
EXPECTED_ZUMBRA_VERSION=0.14.3 \
  scripts/test-z23-compatibility.sh
```

O gate valida:

- SHA-256 das fixtures;
- 151 opcodes oficiais;
- formatter e linter;
- análise do projeto;
- **75 testes**;
- documentação;
- execução VM e C11;
- paridade VM/native;
- Mapper 227 no aplicativo desktop headless;
- rejeição explícita do Mapper 5;
- save RAM, save states e debugger;
- AppDir e `.deb`;
- ausência de C local e ROM comercial;
- higiene do repositório.

Resultado final:

```text
Zumbra NES repository hygiene checks passed.
Z23 compatibility, persistence and debugger gate passed.
```

## Empacotamento

```bash
scripts/package-z23-linux.sh
```

Artefatos principais:

```text
dist/zumbra-nes-0.5.8-linux-amd64.AppDir/
dist/zumbra-nes_0.5.8_amd64.deb
dist/SHA256SUMS-Z23.txt
```

## Roadmap

- Z19 / `0.1.0`: fundação e Mapper 0;
- Z20 / `0.2.0`: CPU 6502;
- Z21 / `0.3.0`: PPU, APU, controles e sincronização;
- Z22 / `0.4.0`: desktop, SQLite e conquistas locais;
- Z23 hotfix / `0.5.8`: latência de input Mapper 227 reduzida com fatias cooperativas sem idle agressivo.
- Z23 hotfix / `0.5.6`: splash inicial, input Mapper 227 mais responsivo e áudio Mapper 227 desativado por segurança.
- Z23 / `0.5.0`: mappers, SRAM, save states, debugger e compatibilidade.

O próximo marco deve priorizar validação de compatibilidade com homebrew/test ROMs legalmente redistribuíveis, refinamento cycle-accurate e suporte a variantes/submappers observados em jogos reais.


## 0.5.6 Mapper 227 input hotfix

The `1200-in-1.nes` Mapper 227 menu uses the normal NES controller polling path. The desktop frontend keeps very short key taps alive for a small host-side window and runs a temporary execution burst when input is active.


## 0.5.8 controles ouvidos no PC

Jogador 1: Start = Enter/Space/keypad Enter; Select = Right Shift/Left Shift/Tab/Backspace; direcional = setas/WASD; A = Z/J; B = X/K; Esc fecha o emulador. Gamepad: A=0, B=1, Select=4, Start=6, D-pad=11-14.
