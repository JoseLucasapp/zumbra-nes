# Zumbra NES 0.4.0 — Z22 playable emulator

A versão 0.4.0 transforma o núcleo headless das Z19–Z21 em um aplicativo desktop jogável para ROMs Mapper 0/NROM.

## Adicionado

- frontend SDL3 com escala inteira 1×–4×, VSync, fullscreen, redimensionamento e letterboxing;
- vídeo RGBA `256×240` e áudio PCM mono a 44,1 kHz;
- teclado, dois gamepads, hot-plug e remapeamento dos dois jogadores;
- abertura por CLI, seletor e ROM recente;
- fechamento de ROM, pausa, reset, avanço de frame, modo ilimitado, mute, volume e FPS;
- biblioteca, configurações, sessões e tempo jogado em SQLite;
- conquistas locais offline com regras de estado, progresso, desbloqueio idempotente e notificações;
- exportação e importação JSON;
- manifesto desktop, ícones, arquivo `.desktop` e AppStream;
- AppDir, `.deb` e suporte a AppImage quando `appimagetool` estiver disponível;
- doze testes novos, totalizando 55;
- gate `scripts/test-z22-playable.sh`.

- frontend integrado somente com APIs oficiais Zumbra, sem fontes C locais ou `extern "C"`;
- correção do evento persistente de frame completo da PPU;
- atualização idempotente das definições de conquistas.

## Compatibilidade

- Zumbra mínima: 0.14.3;
- Linux amd64;
- backend VM e C11;
- frontend jogável: Mapper 0/NROM;
- nenhuma ROM comercial distribuída.

## Gate

```bash
EXPECTED_ZUMBRA_VERSION=0.14.3 scripts/test-z22-playable.sh
```
