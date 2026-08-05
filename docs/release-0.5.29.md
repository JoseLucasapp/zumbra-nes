# zumbra-nes 0.5.29 — launcher, Mapper 10 and Zebra Platformer fixture

## Objetivo

Transformar a 0.5.28 em uma versão testável no desktop real: sem ROM o aplicativo deixa de ser uma tela morta, a ROM 1200-in-1 recebe assistência de Start+Select e o repositório passa a incluir uma ROM homebrew própria para validar vídeo/input sem depender de ROM comercial.

## Mudanças

- `./build/zumbra-nes` sem argumentos abre a tela `NO ROM`; `O`, `Enter` ou `Space` abre o seletor de ROM e `Z` inicia `fixtures/homebrew/zebra-platformer.nes`.
- `./build/zumbra-nes --zebra` inicia diretamente a micro ROM de plataforma da zebra.
- Mapper 10/MMC4 foi adicionado ao núcleo inicial de compatibilidade.
- Mapper 227 ganhou assistência de Start+Select nos menus de multicart e buffers curtos maiores para ações/direcional.
- O gate de mapper incompatível agora valida a mensagem impressa, sem depender de exit code não-zero.
- O gate confere que a ROM Zebra gerada bate com o fixture versionado.

## Controles da Zebra Platformer

- D-pad/setas/WASD: mover.
- A/Z/J: pular.
- Esc: fechar o emulator.

## Status

Validado aqui apenas em estrutura de arquivos, geração do fixture e checksums. A execução real precisa ser feita no Debian com `zumbra 0.14.3`.
