# Frontend desktop Z22

O frontend é implementado integralmente em Zumbra, principalmente em `src/frontend/desktop.zum` e `src/frontend/native_bridge.zum`. Não existem fontes `.c/.h` nem declarações `extern "C"` no repositório.

A Zumbra 0.14.3 fornece as APIs oficiais de framebuffer RGBA, áudio PCM, teclado, gamepads, VSync, argumentos do processo, tempo Unix e criação de arquivos. O runtime oficial carrega SDL3 dinamicamente; por isso o modo visual exige `libsdl3-0`, mas os detalhes nativos não fazem parte da aplicação.

## Pipeline de frame

1. o scheduler executa um frame do console;
2. a PPU fornece 61.440 índices de paleta;
3. `core/palette.zum` converte para 245.760 bytes RGBA;
4. `desktopWindowPresentRGBA` apresenta o framebuffer;
5. o runtime aplica escala e letterboxing;
6. as amostras novas da APU são drenadas e enviadas por `desktopAudioQueue`.

## Fluxo de ROM

A ordem de resolução é:

1. caminho recebido pela linha de comando;
2. fixture sintética executável apenas no modo headless;
3. seletor oficial `desktopPickFile` no modo visual.

Sem argumento, o frontend visual abre o seletor e não executa automaticamente uma fixture de parser. A fixture `z22-playable-loop.nes` possui um loop 6502 válido e vetores RESET/NMI/IRQ definidos.

Arquivos inválidos e mappers diferentes de Mapper 0 produzem mensagem compreensível.

## Modo headless do desktop

`ZUMBRA_DESKTOP_HEADLESS=1` seleciona o backend headless oficial, executa dois frames reais da CPU, usa SQLite em memória e encerra. Esse modo valida a integração do aplicativo em CI sem display, SDL3 ou dispositivo de áudio.
