# Zumbra NES 0.5.7 — Mapper 227 low-latency input hotfix

A 0.5.7 corrige a regressão prática da 0.5.6 na ROM real `1200-in-1.nes`: os botões eram detectados pelo host, mas eram perdidos antes da ROM ler o controle NES.

## Correções

- Remove o caminho de idle automático do Mapper 227 durante execução interativa.
- Troca as fatias enormes de execução por fatias curtas e cooperativas de 8192 instruções.
- Remove o `sleepMs(4)` entre fatias incompletas do Mapper 227.
- Aumenta a janela de retenção de toques rápidos de 12 para 24 ciclos do frontend.
- Mantém áudio Mapper 227 mutado por segurança até uma etapa dedicada de APU/timing.

## Controles ouvidos no PC

Jogador 1:

- Start: Enter, Space, keypad Enter.
- Select: Right Shift, Left Shift, Tab, Backspace.
- Direcional: setas ou WASD.
- A: Z ou J.
- B: X ou K.
- Esc: fecha o emulador.

Gamepad:

- A: botão 0.
- B: botão 1.
- Select: botão 4.
- Start: botão 6.
- D-pad: botões 11, 12, 13 e 14.

## Observação

Esta versão prioriza responsividade sobre economia de CPU para Mapper 227. O consumo pode ser maior do que em um idle agressivo, mas os botões deixam de ser perdidos pelo menu multicart.
