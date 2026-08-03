# Testes Z22

Todas as ROMs versionadas são fixtures sintéticas e não contêm conteúdo comercial.

## Totais

- 10 testes herdados da Z19;
- 13 testes de CPU da Z20;
- 20 testes de hardware da Z21;
- 12 testes adicionados na Z22;
- **55 testes totais**.

## Testes Z22

- `palette_test.zum`: conversão dos índices de paleta para RGBA;
- `audio_output_test.zum`: cursor e drenagem incremental de PCM;
- `settings_test.zum`: defaults e serialização das preferências;
- `store_migration_test.zum`: migrações, versão e integridade SQLite;
- `store_library_test.zum`: biblioteca, sessões e recentes;
- `achievement_engine_test.zum`: regras e desbloqueio;
- `achievement_progress_test.zum`: persistência e idempotência;
- `achievement_frame_boundary_test.zum`: um frame desbloqueia apenas a conquista de primeiro frame;
- `store_export_test.zum`: snapshot e exportação JSON;
- `store_import_test.zum`: importação de configurações e biblioteca;
- `playable_headless_test.zum`: vídeo, áudio, SQLite e conquista no relatório determinístico;
- `playable_rom_execution_test.zum`: execução de um frame da fixture jogável sem opcode de preenchimento.

## Gate completo

```bash
EXPECTED_ZUMBRA_VERSION=0.14.3 scripts/test-z22-playable.sh
```

O gate valida:

1. SHA-256 das fixtures;
2. tabela e decoder dos 151 opcodes oficiais;
3. ausência de `.c`, `.h` e `extern "C"` no projeto;
4. formatter e linter;
5. versão `0.4.0`;
6. análise completa do projeto;
7. os 55 testes pela VM;
8. geração da documentação;
9. execução headless pela VM;
10. build e execução C11 do núcleo headless;
11. paridade exata VM/native;
12. `app doctor`;
13. build e smoke do frontend com `ZUMBRA_DESKTOP_HEADLESS=1`;
14. geração e inspeção de AppDir e `.deb`;
15. higiene do repositório.

Resultado esperado:

```text
Zumbra NES repository hygiene checks passed.
Z22 playable emulator gate passed.
```

## Teste manual desktop

O CI não substitui a validação visual e sonora em uma máquina com SDL3. Antes da promoção final, validar janela, escala, vídeo, áudio, teclado, gamepads, remapeamento, hot-plug, controles de execução, SQLite, conquistas e pacotes.

## AppImage

O caminho de empacotamento está implementado, mas depende de `appimagetool`. Quando a ferramenta não está disponível, AppDir e `.deb` continuam sendo validados.
