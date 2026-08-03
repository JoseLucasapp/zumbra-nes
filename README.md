# Zumbra NES

Fundação concluída de um emulador NES/Famicom escrita em **Zumbra 0.14.2**.

A Z19 está tecnicamente fechada quando o gate completo compila o projeto pelo backend C11, executa o binário nativo e confirma paridade byte a byte com a execução pela VM.

A versão `0.1.0` corresponde ao marco **Z19**. Ela implementa a infraestrutura de cartucho e memória necessária para a CPU 6502 que será desenvolvida no Z20, sem incluir ROMs comerciais.

## Implementado no Z19

- leitura segura de arquivos binários;
- validação do cabeçalho `NES<EOF>`;
- parser iNES 1.0;
- identificação e parsing linear básico de NES 2.0;
- estrutura `Cartridge`;
- trainer de 512 bytes;
- Mapper 0/NROM-128 e NROM-256;
- mapa de memória da CPU;
- RAM interna e espelhamentos;
- registradores PPU/APU como contratos de integração;
- PRG RAM e PRG ROM;
- relógio determinístico 3:1 entre PPU e CPU;
- frontend headless de diagnóstico;
- persistência de metadados em JSON;
- ROMs sintéticas e testes executáveis.

## Requisitos

- Zumbra `0.14.2` disponível no `PATH`;
- Linux para o gate nativo completo desta primeira versão;
- `clang` ou `gcc` e dependências nativas exigidas pelo backend Zumbra.

## Teste rápido

```bash
zumbra project check
zumbra project test
zumbra project run
```

Gate completo:

```bash
scripts/test-z19-foundation.sh
```

O relatório da validação desta entrega está em [`VALIDATION.md`](VALIDATION.md).

O gate completo é o critério oficial da Z19. Para uma verificação rápida, sem substituir a aprovação nativa:

```bash
Z19_SKIP_NATIVE=1 scripts/test-z19-foundation.sh
```

## ROMs

O repositório aceita somente ROMs sintéticas, homebrew com redistribuição permitida ou dumps produzidos legalmente pelo próprio usuário. Nenhuma ROM comercial é incluída.

## Estado de conclusão

- parser, cartucho, Mapper 0, barramento, clock, persistência e frontend headless concluídos;
- 10 testes de projeto concluídos;
- execução VM concluída;
- build e execução nativos validados pelo gate completo;
- próxima ação de repositório: commit inicial, push para `JoseLucasapp/zumbra-nes` e tag `v0.1.0`.

## Próximo marco

O Z20 implementará a CPU 6502, tabela oficial de opcodes, modos de endereçamento, interrupções, ciclos e testes de conformidade.
