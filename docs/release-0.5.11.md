# Zumbra NES 0.5.11 — cooperative Mapper 227 scheduler

A 0.5.11 troca a estratégia agressiva de rodar um frame inteiro do Mapper 227 em um único burst por um scheduler cooperativo.

## Problema corrigido

Na ROM real `1200-in-1.nes`, a 0.5.10 ficou mais rápida que as versões anteriores, mas ainda podia bloquear o desktop quando a ROM entrava em uma rotina pesada após selecionar um jogo interno. O sintoma era input com delay restante, janela preta e o PC aparentando travar.

## Correção

- o Mapper 227 agora roda em microfatias de instruções;
- o frontend respeita um orçamento curto de tempo de host por iteração;
- eventos SDL são drenados entre microfatias;
- o controle do jogador 1 é mantido por uma janela maior e reaplicado durante o trabalho cooperativo;
- frames uniformes pretos/cinzas não são apresentados como saída final enquanto a ROM não produzir frame visível real;
- o áudio continua desabilitado para Mapper 227 até uma etapa própria de APU/timing.

## Critério de aprovação manual

Com `1200-in-1.nes`, a janela deve continuar responsiva ao alternar itens no menu e ao abrir um jogo interno. `Esc` deve fechar sem precisar matar o processo externamente.
