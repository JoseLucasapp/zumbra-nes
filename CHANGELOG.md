## 0.5.63 — Game Library and achievement UI

- Adds a complete in-emulator Game Library backed by the existing local SQLite database.
- Replaces the single Recent ROM launcher entry with a browsable library while preserving direct Load ROM.
- Adds search, five library filters (`ALL`, `KNOWN`, `IN PROGRESS`, `COMPLETED`, `NO PACK`) and five sort modes (`RECENT`, `TITLE`, `PROGRESS`, `PLAY TIME`, `SESSIONS`).
- Adds per-ROM rows showing achievement completion, play time and missing-file state.
- Adds a Game Details screen with mapper, SHA-256 identity prefix, ROM availability, achievement completion, play time, session count and relative last-played status.
- Adds a dedicated per-game achievement browser with `ALL`, `LOCKED` and `UNLOCKED` views.
- Adds full keyboard/gamepad navigation for library, details and achievement views; F2/F3/F4 provide filter/sort/search shortcuts.
- Makes the main Achievements entry open the known-games achievement library instead of a placeholder panel.
- Adds F9 local JSON export from the library achievement browser.
- Adds SQLite schema version 6 indexes for library title/play-time/session queries while preserving existing local progress.
- Separates monotonic SDL timing from persisted wall-clock timestamps: sessions, last-opened, save-state metadata and new achievement unlocks now use `unixTimeSeconds()`. Existing 0.5.62 tick-based rows remain readable and are labeled `LEGACY` until replayed.
- Adds `src/frontend/library.zum` as the library view-model layer and `tests/game_library_test.zum` covering search, filters, sorting state, progress, sessions and display helpers.
- Raises the direct release test inventory to 84 files and keeps Zumbra-lang frozen at 0.14.5.

## 0.5.62 — local achievements offline

- Adds a complete local-only achievements layer backed by SQLite.
- Keeps achievements on the user's PC with no account, cloud sync, leaderboard or remote server.
- Adds local achievement game metadata, progress summaries, unlock events and backup/export helpers.
- Adds `F6` achievements overlay, `F9` local JSON export, an `E` export fallback inside F6 and SQLite save-state metadata recording.
- Adds local achievement install, summary, export/import and monotonic progress tests.
- Keeps Zumbra-lang pinned to 0.14.5 and preserves Z28 mapper compatibility.
- Keeps achievement SQLite work after audio queueing and suppresses unchanged progress writes.
- Fixes the live desktop PCM boundary: samples are compressed to the byte range expected by the frozen 0.14.5 S16 bridge, then resampled from the established APU /40 stream to exactly 44.1 kHz without changing APU timing.
- Replaces the placeholder F6 panel with real per-ROM achievement rows, explicit game goals, locked progress, unlocked state and named unlock toasts.
- Makes all emulator-facing status/remap/compatibility text English.
- Removes procedural emulator-use achievements for unknown games; no more `use A`, `play N seconds`, frame-count or CPU-count goals presented as game achievements.
- Adds CRC-32 ROM recognition alongside SHA-256 persistence identity so known iNES header variants resolve the same bundled game pack.
- Bundles 8 game-specific achievements for Nintendo Tetris and 8 for Nintendo Popeye, based on each game's documented work-RAM state.
- Removes development-phase labels from the production UI/runtime and keeps only the public emulator version.
- Makes the main-menu Controls entry functional with in-window remapping/reset and automatic vendor-neutral SDL Gamepad input.
- Fixes external controller polling to use the runtime's 1-based gamepad slots, polling both available slots instead of an invalid slot 0.
- Removes Xbox-specific wording; supported SDL gamepads hot-plug automatically regardless of vendor mapping.
- Makes Escape edge-triggered: overlays go back, gameplay returns to the emulator menu, and only Quit/F12/window-close exits the app.
- Fixes the final achievement-engine test typing regression by passing explicit `u8` RAM bytes to `bus.write`.
- Reworks keyboard remapping into a non-blocking in-window capture flow so the overlay remains visible while waiting for the new key.
- Displays normal A-Z/0-9/common-key names instead of the ambiguous `SC` placeholder, and makes remapping replace the old binding instead of keeping hidden fallback keys active.
- Keeps Zumbra 0.14.5 aggregate `project test` diagnostics opt-in; the normal release gate executes the authoritative 83 `*_test.zum` files directly without printing the known 119-file unused-symbol precheck failure.

## 0.5.61 — Z28 compatibility and mapper expansion

- Expands the supported mapper registry from 8 to 15 mapper families.
- Adds Mapper 11/Color Dreams, 30/UNROM 512, 66/GxROM, 71/Camerica, 87/Jaleco, 94/UN1ROM and 180/UNROM reverse.
- Adds mapper expansion and diagnostics regression tests.
- Adds a compatibility matrix for supported mapper behavior and limits.
- Keeps Zumbra-lang pinned to 0.14.5 and preserves Z27 settings persistence, audio, input, save states and desktop UX.

## 0.5.60 — Z27 typed settings persistence

- Reintroduced durable desktop settings through the existing SQLite settings table.
- Kept control values as typed integers in memory and stringified values only at the store boundary.
- Persisted audio ON/OFF through the existing `muted` setting.
- Added fallback behavior for corrupted numeric settings.
- Added `tests/settings_persistence_test.zum`.

## 0.5.53 — audio cleanup

- Cleaned live desktop audio with a light 3-tap low-pass filter.
- Softened chunk edges to reduce SDL queue pops/static.
- Raised the queue guard from 8192 to 12288 bytes to reduce starvation.

## 0.5.53 — in-window controls and Xbox gamepad

- Moves Settings from terminal output to an in-window overlay rendered over the emulator frame.
- Remapping keys `1`-`8` now only works while Settings is open, preventing accidental freezes during gameplay.
- Adds an input-release lock after ROM/start/settings transitions to avoid stuck Enter/D-pad state.
- Adds automatic Xbox-style gamepad polling through the native desktop bridge.

## 0.5.53

- Fix desktop Settings build failure caused by `data` module alias collision.
- Preserve runtime-editable controller mapping from 0.5.53.

# 0.5.53 - input settings hotfix

- Added runtime controller settings in the desktop frontend.
- F1 shows current bindings; 1-8 remap actions; F2 resets defaults.
- Bindings persist in `zumbra-nes-controls.json`.
- Removed hidden aliases/action buffering from the real emulator loop.

## 0.5.53 — smooth-frame fast PPU and Zumbra 0.14.5

- Requires Zumbra 0.14.5 so native string literals use `z_string_static(...)` instead of allocating heap strings every time a literal is evaluated.
- Removes the artificial desktop render stride for Mapper 10 and Mapper 227; completed frames are presented instead of intentionally skipped.
- Changes the desktop fast PPU path to render visible scanlines at stable scanline boundaries.
- Clocks mapper scanline/latch events inside the fast PPU path to reduce lower-screen flicker in MMC/MMC4-style games.
- Keeps live APU ticking disabled in desktop performance mode while video throughput is stabilized.

## 0.5.29 — ROM launcher, Mapper 10 and Zebra homebrew test ROM

- Adds a no-ROM launcher path: O/Enter opens a ROM picker, Z starts the built-in Zebra Platformer fixture.
- Adds initial Mapper 10/MMC4 support so mapper-10 `.nes` files can enter the emulator instead of being rejected.
- Adds `fixtures/homebrew/zebra-platformer.nes`, an original NROM/CHR-RAM micro platformer used to test video and controller input without commercial ROMs.
- Adds Start+Select assist for Mapper 227 multicart menus and longer short-tap buffers for D-pad/actions.
- Fixes the unsupported-mapper desktop smoke so it validates the incompatibility message instead of relying on process exit status.

## 0.5.29 — desktop intro and input stabilization

- Mostra uma tela sem ROM após a intro em vez de ficar apenas no logo.
- Prolonga a intro antes de carregar ROMs reais.
- Corrige retorno de mapper incompatível para o smoke de desktop.
- Adiciona buffer curto de input para A/B/Select/Start e pulso curto no D-pad.

## 0.5.29 — desktop app-build return fix

- Corrige `zumbra app build` falhando com `types: function has conflicting return types: null and bool`.
- Torna explícitos os retornos em `src/frontend/desktop.zum` e `src/frontend/native_bridge.zum`.
- Mantém o runner individual de testes da 0.5.23.

## 0.5.23 — project-check gate unblock and stable desktop shell

- Makes project check advisory in the Z23 gate because the current warning-only diagnostics were blocking the release loop.
- Keeps later project test/build/smoke checks blocking.
- Simplifies the desktop frontend to the stable shell path only.

## 0.5.23 — safe no-ROM shell, bitmap intro and hard Mapper 227 guard

- Avoids the experimental UI panel path that crashed with `field access requires a struct or enum type` when launching without a ROM.
- Uses `assets/zumbra-nes.bmp` for the startup intro so the logo is not misspelled by block-glyph rendering.
- Starts Mapper 227 ROMs paused in safe mode and requires explicit unpause, reducing the chance of freezing the desktop.

# Changelog

## 0.5.23 — safe shell, input guard and Mapper 227 throttle

- Replaces synthetic controller hold with direct live input to stop infinite auto-scroll.
- Adds a startup menu panel covering ROM open, controls, video/GPU, CPU/execution and library shortcuts.
- Simplifies the intro to a still Zumbra logo screen.
- Starts without forcing the file picker when no ROM argument is provided.
- Runs Mapper 227 in a strict host-safe scheduler with a no-frame watchdog and mandatory yield.
- Prioritizes keeping the PC responsive over brute-forcing the 1200-in-1 black-screen path.

## 0.5.23

- Requires the Zumbra 0.14.3 native method hot-loop compiler patch.
- Adds a gate check for direct method dispatch in generated C.
- Keeps Mapper 227 under a conservative cooperative scheduler to avoid desktop lockups.
- Documents the 1200-in-1 stability fix path.

## 0.5.23 — Mapper 227 OOM guard and reusable framebuffer

- Reused the desktop RGBA framebuffer to avoid repeated 256x240x4 allocations.
- Added allocation-light `console.runFrameSliceCode` for the desktop hot loop.
- Added a black-screen guard for Mapper 227 internal game launches.
- Added a lightweight startup intro before command-line ROM execution.
- Kept mapper 10 unsupported; Z23 supports mappers 0, 1, 2, 3, 4, 7 and 227.

## 0.5.23

- Removes the desktop splash framebuffer path that could trigger `value is not callable` in real SDL command-line ROM launches.
- Tightens Mapper 227 cooperative scheduler budget to keep the host responsive while internal games boot.

## 0.5.23 — Z23 desktop runtime callable fix and safe splash inline

- Fixes a desktop-only runtime failure after the gate passed: `zumbra runtime error: value is not callable`.
- Removes the module-level splash call from the interactive hot path and inlines the splash renderer in `desktop.zum`.
- Keeps the 0.5.11 cooperative Mapper 227 scheduler so the host keeps processing SDL events while the multicart is running.
- Does not change Zumbra-lang; this version expects Zumbra 0.14.3 with the native hot-loop safe fix.

## 0.5.11 — Z23 Mapper 227 cooperative scheduler and freeze guard

- Substitui o burst monolítico de 240.000 instruções do Mapper 227 por fatias cooperativas menores com orçamento de host por iteração.
- O frontend agora drena eventos SDL entre microfatias, evitando que a janela e o desktop sejam marcados como travados.
- Mantém botões retidos por mais tempo, mas reavalia input durante a execução, reduzindo perda de Start/Select/D-pad.
- Não apresenta frames uniformes pretos/cinzas do Mapper 227; mantém splash/intro até haver framebuffer visível real.
- Adiciona validação manual específica contra regressão de tela preta e congelamento no `1200-in-1.nes`.

## 0.5.10 — Z23 Mapper 227 low-latency input hotfix

- Removed the automatic Mapper 227 idle path that starved real multicart menus.
- Replaced huge input-boost slices with short cooperative slices so SDL polling runs frequently.
- Removed the per-slice sleep while Mapper 227 is still producing the next frame.
- Extended short key taps so the ROM has enough controller-read windows to observe them.
- Documented the exact keyboard/gamepad buttons heard by the desktop frontend.


## 0.5.10

- Mapper 227 performance/input hotfix for the real `1200-in-1.nes` menu.
- Disabled Mapper 227 APU ticking while audio remains muted.
- Added PPU render skipping for intermediate Mapper 227 frames while preserving timing/NMI.


## 0.5.10 — Z23 responsiveness hotfix

- Added cooperative desktop emulation slices so SDL events are drained while a frame is being emulated.
- Added bounded event draining and short host yields to prevent the window manager from marking the emulator as not responding.
- Kept Mapper 227 compatibility, SRAM, save states and debugger behavior from 0.5.0.

## 0.5.0 — Z23 compatibility, persistence and debugger

- arquitetura mutável e compartilhada de mappers para CPU e PPU;
- Mapper 1/MMC1, Mapper 2/UxROM, Mapper 3/CNROM, Mapper 4/MMC3, Mapper 7/AxROM e Mapper 227;
- bank switching PRG/CHR, mirroring, PRG RAM e IRQ de MMC3;
- fórmulas de latch e proteção de CHR RAM do Mapper 227;
- SRAM de bateria persistida por SHA-256 da ROM;
- dez slots de save state com validação de schema, versão, ROM e mapper;
- snapshots de CPU, PPU, APU, bus, RAM, OAM, controles, DMA, clock e mapper;
- debugger com step, breakpoints, memória, stack, disassembly, mapper e trace;
- migração SQLite 4 e metadados de save states;
- fixture visual Mapper 0, fixture Mapper 227 e fixture de mapper incompatível;
- diagnóstico estruturado de compatibilidade e falha explícita para mappers não suportados;
- dezenove testes novos, totalizando 74;
- gate Z23 com VM/C11, desktop headless, Mapper 227, incompatibilidade, AppDir e `.deb`.

## 0.4.0 — Z22 playable emulator

- frontend SDL3 jogável para Mapper 0/NROM;
- framebuffer PPU convertido para RGBA e áudio PCM da APU enviado ao dispositivo;
- escala inteira 1×–4×, letterboxing, VSync, fullscreen e redimensionamento;
- teclado, dois gamepads, hot-plug e remapeamento dos dois jogadores;
- abertura por CLI, seletor e recentes, além de fechamento de ROM;
- pausa, reset, avanço de frame, velocidade ilimitada, FPS, volume e mute;
- SQLite para configurações, biblioteca, sessões, tempo jogado e conquistas;
- regras locais de conquistas, progresso idempotente e notificações;
- exportação/importação JSON;
- AppDir, `.deb` e caminho de AppImage via `appimagetool`;
- integração desktop escrita somente em Zumbra sobre as APIs oficiais de mídia da Zumbra 0.14.3;
- removida a ponte local `native/z22_desktop.c` e todas as declarações `extern "C"`;
- correção do latch `frameComplete` da PPU, que agora permanece ativo até ser consumido pelo scheduler;
- definição de conquistas atualizada por UPSERT e conquista de instruções movida para 100.000 instruções;
- doze testes novos, totalizando 55, e gate Z22 com VM/C11.

## 0.3.0 — Z21

- PPU Ricoh 2C02 com registradores CPU, VRAM, palette, OAM e framebuffer 256×240.
- Background, attribute tables, scroll, sprites 8×8/8×16, prioridade, flip, sprite zero hit e overflow.
- Scanlines/dots, VBlank, NMI e odd-frame skip.
- OAM DMA em `$4014` com stalls de 513/514 ciclos.
- Dois controles NES com strobe e shift serial.
- APU com pulse 1/2, triangle, noise e DMC.
- Envelopes, sweep, length/linear counters, frame sequencer, IRQs e buffer PCM.
- Scheduler integrado de CPU, PPU e APU, incluindo DMA, DMC e linhas de interrupção.
- Vinte testes de hardware adicionados, totalizando 43 arquivos de teste.
- Frontend headless atualizado com digests de frame e áudio.
- Gate Z21 com paridade VM/C11.

## 0.2.0 — Z20

- CPU Ricoh 2A03/NMOS 6502 completa no escopo de opcodes oficiais.
- 151 opcodes oficiais, modos de endereçamento, stack, vetores, IRQ/NMI e ciclos.
- Treze novos testes de CPU e 23 testes totais.
- Gate Z20 com paridade VM/C11.

## 0.1.0 — Z19

- Fundação do emulador NES/Famicom.
- iNES/NES 2.0 básico, cartucho, Mapper 0, bus, clock, fixtures e frontend headless.

## 0.4.0 — correção pré-release

### Correções de validação pré-release

- o frontend interativo não inicia mais automaticamente uma fixture sintética de teste;
- o modo headless agora executa instruções reais da CPU durante um frame completo;
- adicionada uma ROM sintética executável e determinística para smoke tests;
- adicionada regressão contra execução acidental do opcode de preenchimento `0xF4`.


## 0.5.23

- Made the Z23 gate execute tests file-by-file when aggregate `project test` stops on warning-only project diagnostics.
- Added `scripts/run-z23-tests.sh` as the authoritative Z23 test execution step.
## 0.5.53 — scheduler de frame, ajuda e CI por versão

- Substitui o teto de 1.024 instruções por um scheduler limitado por tempo capaz de completar frames NES em velocidade útil.
- Mantém Mapper 227 cooperativo, com fatias menores e polling frequente do SDL.
- Adiciona ajuda de controles em C/H e documenta o mapa oficial da versão.
- Ativa CI em `main`, pull requests, tags versionadas e execução manual.
- Corrige os gates de oito mappers, 76 testes, ROM homebrew e SQLite local ignorado.

### Z29 stabilization follow-up
- Unknown ROMs now receive a deterministic procedural achievement pack derived from ROM SHA-256 and cartridge metadata instead of an empty F6 screen.
- Curated per-game packs still take precedence when exact game semantics are known.
- Generated packs are identical for the same ROM across players/PCs but differ across ROM hashes.
- Generated achievement rows show current/target progress and explicit units/goals instead of vague labels.
- Reverted the experimental Z29 APU rescaling/fractional sample-clock changes to the last 0.5.61-derived audio path after real-device validation reported severely dragged audio.
