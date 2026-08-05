# zumbra-nes 0.5.25 — desktop null-return pipeline fix

Objetivo: corrigir o bloqueio do `zumbra app build` no frontend desktop após o headless nativo passar.

Mudanças principais:

- `desktop.run()` não retorna mais `bool`; todos os caminhos terminam com retorno nulo.
- Caminhos de erro do desktop real deixam de chamar `panic(...)` no startup e encerram de forma controlada.
- Gate atualizado para 0.5.25.
- Mantém o runner individual de testes da Z23.

Critério: o gate deve avançar do build headless para `zumbra app build` e gerar `build/zumbra-nes`.
