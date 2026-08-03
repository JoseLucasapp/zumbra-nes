# Zumbra NES

Emulador NES/Famicom em desenvolvimento, escrito em **Zumbra 0.14.2**.

A versão `0.2.0` conclui o marco **Z20**: a CPU Ricoh 2A03/NMOS 6502 está implementada em nível de instrução, integrada ao barramento criado na Z19 e validada pela VM e pelo backend C11 nativo.

A Z20 não inclui PPU, APU, controles reais ou janela jogável. Esses componentes pertencem aos próximos marcos.

## Implementado

### Z19 — fundação

- parser iNES 1.0 e identificação básica de NES 2.0;
- cartucho, trainer, PRG ROM/RAM e CHR ROM/RAM;
- Mapper 0 com NROM-128 e NROM-256;
- barramento, espelhamentos e vetores;
- scheduler determinístico de CPU/PPU;
- frontend headless, persistência e fixtures sintéticas.

### Z20 — CPU 6502

- registradores `A`, `X`, `Y`, `SP`, `PC` e status;
- flags `C`, `Z`, `I`, `D`, `B`, `U`, `V` e `N`;
- reset pelos vetores do cartucho;
- 151 opcodes oficiais do NMOS 6502;
- todos os modos de endereçamento oficiais;
- fetch, decode e execute;
- aritmética, lógica, comparação, carga, armazenamento e transferências;
- operações de stack e controle de fluxo;
- `BRK`, `RTI`, `JSR`, `RTS`, `IRQ` e `NMI`;
- penalidades de ciclo por page crossing e branches;
- bug de wrap do `JMP ($xxFF)` reproduzido;
- flag decimal preservada, com `ADC`/`SBC` binários como no Ricoh 2A03;
- rejeição controlada de opcode ilegal;
- metadados públicos da tabela de opcodes;
- integração determinística com o clock da Z19;
- paridade de saída entre VM e executável C11.

## Requisitos

- Zumbra `0.14.2` no `PATH`;
- Linux para o gate nativo oficial atual;
- `clang` ou `gcc`;
- dependências nativas exigidas pelo backend Zumbra.

Confirme a versão:

```bash
zumbra --version
```

Resultado esperado:

```text
0.14.2
```

## Testes

Verificação rápida:

```bash
zumbra project check
zumbra project test
zumbra project run
```

Gate oficial da Z20:

```bash
scripts/test-z20-cpu.sh
```

O gate executa formatter, linter, pipeline, 23 testes, documentação, VM, build nativo, execução nativa, comparação VM/native e higiene.

O script histórico `scripts/test-z19-foundation.sh` encaminha para o gate atual; a implementação original da Z19 permanece preservada na tag `v0.1.0`.

Para diagnóstico sem o build C11, sem substituir a aprovação oficial:

```bash
Z20_SKIP_NATIVE=1 scripts/test-z20-cpu.sh
```

## Saída headless

O programa principal carrega uma fixture NROM sintética, reseta a CPU, executa `LDA #$01` e `NOP` e imprime um relatório estável. Entre os valores esperados estão:

```text
Zumbra NES Z20 CPU 6502
A = 1
PC = $8003
instruções = 2
ciclos CPU = 11
ciclos PPU = 33
```

## ROMs

O repositório aceita somente ROMs sintéticas, homebrew com redistribuição permitida ou dumps produzidos legalmente pelo próprio usuário. Nenhuma ROM comercial é incluída.

## Estado

- Z19: concluída e publicada como `v0.1.0`;
- Z20: CPU 6502 completa no escopo oficial e versão `0.2.0`;
- próximo marco: Z21, com PPU, APU, controllers e sincronização de hardware.

Detalhes técnicos estão em [`docs/cpu6502.md`](docs/cpu6502.md), e os critérios de conclusão em [`docs/z20-completion.md`](docs/z20-completion.md).
