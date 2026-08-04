# Fechamento da Z22

A Z22 entrega o primeiro frontend desktop jogável do `zumbra-nes` para Mapper 0/NROM.

## Critérios técnicos

- [x] frontend SDL3;
- [x] integração desktop somente em Zumbra, sem `.c/.h` ou `extern "C"`;
- [x] framebuffer RGBA `256×240`;
- [x] escala inteira, redimensionamento e letterboxing;
- [x] fullscreen e VSync;
- [x] áudio PCM em dispositivo real;
- [x] volume e mute;
- [x] teclado e dois gamepads;
- [x] hot-plug;
- [x] remapeamento dos dois jogadores;
- [x] abrir ROM por CLI, seletor e recente;
- [x] fechar ROM;
- [x] pausa, reset e avanço de frame;
- [x] modo ilimitado e FPS;
- [x] SQLite local;
- [x] biblioteca, sessões e tempo jogado;
- [x] conquistas offline e notificações;
- [x] exportação e importação JSON;
- [x] 55 testes;
- [x] paridade VM/C11 do smoke headless;
- [x] build desktop headless;
- [x] AppDir e `.deb`;
- [x] gate Z22 e CI configurados.

## Critérios de promoção

Ainda devem ser executados na máquina de desenvolvimento:

- [ ] gate oficial com a CLI publicada;
- [ ] validação visual, sonora e de gamepads com SDL3;
- [ ] instalação real do `.deb`;
- [ ] geração e execução do AppImage com `appimagetool`;
- [ ] commit e push;
- [ ] CI verde da branch e da tag;
- [x] tag `v0.4.0`;
- [x] Release `0.4.0`.

A ausência de `appimagetool` não invalida o código de AppDir/`.deb`, mas o AppImage deve ser produzido antes de declarar a distribuição Linux completa.


## Correção pré-release da inicialização

O frontend interativo não usa mais a fixture de parser como ROM inicial. Sem argumento, o seletor de ROM é aberto. O modo headless usa uma fixture executável dedicada e executa um frame real da CPU, fechando a lacuna detectada durante a validação manual do desktop.

## Correção final pré-release

- [x] fixture de inicialização com loop 6502 válido;
- [x] `frameComplete` permanece ativo até ser consumido;
- [x] conquista de instruções não conflita com o primeiro frame;
- [x] definições de conquistas são atualizadas por UPSERT;
- [x] ponte C removida do repositório;
- [x] baseline atualizada para Zumbra 0.14.3.
