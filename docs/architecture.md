# Arquitetura Z22

## Visão geral

```text
ROM iNES/NES 2.0
        │
        ▼
Cartridge → Mapper 0/NROM → Bus
                            ├─ CPU Ricoh 2A03
                            ├─ PPU Ricoh 2C02 → framebuffer 256×240
                            ├─ APU → ring buffer PCM
                            ├─ Controller 1/2
                            └─ OAM DMA / DMC fetch
                                      │
                                      ▼
                              Console scheduler
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                 Frontend headless          Frontend desktop
                 VM/C11 parity              Zumbra runtime + SDL3 + SQLite
```

## Núcleo de emulação

- `src/core/header.zum`: leitura e validação iNES e identificação NES 2.0;
- `src/core/cartridge.zum`: PRG, CHR, trainer e metadados;
- `src/core/mapper.zum`: Mapper 0, NROM-128 e NROM-256;
- `src/core/bus.zum`: mapa CPU, PPU, APU, controles, DMA e cartridge;
- `src/core/cpu6502.zum`: 151 opcodes oficiais, interrupções e ciclos;
- `src/core/ppu.zum`: registradores, VRAM, OAM, render, VBlank e NMI;
- `src/core/apu.zum`: pulse 1/2, triangle, noise, DMC, IRQ e PCM;
- `src/core/controller.zum`: dois controles NES serializados;
- `src/core/console.zum`: scheduler CPU/PPU/APU, DMA, DMC e interrupções;
- `src/core/palette.zum`: conversão dos índices PPU para RGBA;
- `src/core/audio_output.zum`: drenagem incremental do ring buffer da APU.

## Scheduler

Cada ciclo retornado pela CPU avança um ciclo da APU e três dots da PPU. O scheduler também:

- aplica OAM DMA de 256 bytes e stall de 513/514 ciclos;
- atende buscas DMC pelo bus e aplica quatro ciclos de stall;
- propaga NMI da PPU e IRQ da APU para a CPU;
- permite execução por instrução, quantidade de ciclos ou frame completo.

## Frontend desktop

`src/frontend/desktop.zum` é o loop de aplicação e `src/frontend/native_bridge.zum` é agora uma fachada **100% Zumbra** sobre o runtime oficial 0.14.3. O repositório não contém `.c`, `.h` nem `extern "C"`.

As APIs oficiais usadas são:

- `desktopApp`, `desktopWindow` e `desktopPoll`;
- `desktopWindowPresentRGBA` para o framebuffer;
- `desktopWindowSetVSync`;
- `desktopKeyDown` e `desktopGamepadButton`;
- `desktopAudioQueue` e `desktopAudioQueued`;
- `desktopPickFile`, `desktopNotify` e `desktopPaths`;
- `processArgs`, `unixTimeSeconds` e `createFile`.

SDL3 e o backend C11 continuam existindo dentro do compilador/runtime da linguagem, como detalhe de implementação. Nenhuma ponte C é distribuída ou mantida pelo projeto do emulador.

## Fluxo de frame

1. o frontend coleta teclado e gamepads;
2. os masks dos dois controles são enviados ao console;
3. o scheduler executa um frame;
4. a PPU fornece 61.440 índices de paleta;
5. `palette.rgba` produz 245.760 bytes RGBA;
6. SDL3 atualiza e apresenta a textura;
7. novas amostras da APU são drenadas e enfileiradas;
8. conquistas são avaliadas e persistidas;
9. FPS, sessão e estado da janela são atualizados.

## Persistência

`src/persistence/store.zum` usa SQLite como fonte de verdade. As migrações criam:

- `settings`;
- `rom_library`;
- `play_sessions`;
- `achievement_definitions`;
- `achievement_progress`.

A ROM é identificada pelo SHA-256, não apenas pelo caminho. JSON é usado exclusivamente para exportação, importação e depuração.

## Conquistas

`src/achievements/engine.zum` avalia regras de frame, instruções, tempo, controle e memória. O desbloqueio é idempotente e vinculado ao digest da ROM.

## Empacotamento

`zumbra-app.toml` descreve o aplicativo desktop. O pipeline Linux produz:

- binário C11;
- AppDir;
- pacote `.deb`;
- AppImage quando `appimagetool` está disponível;
- checksums SHA-256.

## Limites atuais

A interface jogável aceita apenas Mapper 0/NROM. Não são distribuídas ROMs comerciais. Save states, mappers adicionais, depuração avançada e validação extensa com homebrew/test ROMs ficam para a Z23.
