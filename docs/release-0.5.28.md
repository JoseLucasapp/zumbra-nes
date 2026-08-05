# Zumbra NES 0.5.29

Foco: estabilização visual e entrada do desktop após a primeira execução real da 0.5.27.

Correções:

- A tela sem ROM deixou de ficar apenas no logo; após a intro, mostra um shell gráfico simples de "NO ROM".
- A intro agora é apresentada por uma janela de tempo real antes de carregar a ROM, evitando o salto visual cinza -> menu.
- O caminho de ROM incompatível volta a retornar falha para o smoke de mapper não suportado.
- Entrada do controle 1 recebeu buffer curto para botões A/B/Select/Start e pulso curto para D-pad, sem reintroduzir hold infinito.
- Mantido o loop cooperativo do Mapper 227 para não monopolizar o sistema.

Critério de aprovação:

1. `scripts/test-z23-compatibility.sh` precisa chegar em `Z23 compatibility, persistence and debugger gate passed.`
2. `./build/zumbra-nes` precisa mostrar intro e depois shell sem ROM.
3. `taskset -c 0 ./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"` precisa mostrar intro e aceitar teclado no menu.
