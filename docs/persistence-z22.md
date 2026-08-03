# Persistência e conquistas Z22

O módulo `src/persistence/store.zum` aplica três migrações SQLite.

## Tabelas

- `settings`: preferências e mapeamento;
- `rom_library`: biblioteca, caminho, mapper e tempo acumulado;
- `play_sessions`: início, fim, segundos e frames;
- `achievement_definitions`: catálogo por SHA-256 da ROM;
- `achievement_progress`: progresso, desbloqueio e data.

A identidade do jogo é o SHA-256 da imagem carregada. Caminhos podem mudar sem perder progresso.

## Regras locais

O engine suporta:

- `frame_count`;
- `instruction_count`;
- `controller_mask`;
- `session_seconds`;
- `memory_equals`;
- `memory_at_least`.

O desbloqueio é idempotente: uma conquista já liberada não é notificada novamente.

## Exportação

`store.exportJson` exporta configurações, biblioteca e progresso. O SQLite continua sendo a fonte de verdade; JSON não substitui o banco.
