# Correção pré-release Z22 — inicialização desktop e smoke real da CPU

A validação manual revelou que o frontend interativo carregava automaticamente a fixture `nrom-128-horizontal.nes`. Essa fixture foi criada para parser/barramento, contém `BRK` logo após o smoke inicial e seu vetor IRQ aponta para um byte de preenchimento `0xF4`, que não pertence aos 151 opcodes oficiais implementados.

A correção:

- adiciona `z22-playable-loop.nes`, uma fixture sintética executável com loop 6502 válido;
- usa a nova fixture apenas em modo headless;
- sem argumento, o frontend interativo abre o seletor de ROM em vez de executar uma fixture de teste;
- o smoke headless passa a executar `runFrame`, portanto executa instruções reais da CPU;
- adiciona uma regressão que executa um frame completo e confirma que a CPU não é interrompida;
- atualiza o gate e a higiene para 54 testes.
