# Zumbra NES 0.5.1 — Z23 responsiveness hotfix

Esta correção mantém o escopo da Z23, mas muda o loop interativo do desktop para não travar o gerenciador de janelas enquanto a CPU, PPU e APU emulam um frame.

## Correções

- execução cooperativa em fatias de instruções;
- drenagem de eventos SDL em lotes limitados por iteração;
- fechamento por Esc e botão da janela passa a ser observado entre fatias;
- pequenas pausas de host quando um frame ainda não terminou, reduzindo disputa agressiva com VS Code/terminal;
- apresentação do framebuffer apenas quando um frame novo fica completo;
- apresentação em pausa limitada a 10 Hz para evitar loop desnecessário;
- preservação da compatibilidade Mapper 227 e do formato de save state `Z23-0.5.0`.

## Dependência

Compatível com Zumbra `0.14.3`. A correção fica no loop desktop do emulador, sem exigir alteração na linguagem.
