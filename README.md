# Zumbra NES

Fundação de um emulador NES/Famicom escrita em **Zumbra 0.14.1**.

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

- Zumbra `0.14.1` disponível no `PATH`;
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

Para pular apenas a compilação C nativa durante uma verificação rápida:

```bash
Z19_SKIP_NATIVE=1 scripts/test-z19-foundation.sh
```

## ROMs

O repositório aceita somente ROMs sintéticas, homebrew com redistribuição permitida ou dumps produzidos legalmente pelo próprio usuário. Nenhuma ROM comercial é incluída.

## Próximo marco

O Z20 implementará a CPU 6502, tabela oficial de opcodes, modos de endereçamento, interrupções, ciclos e testes de conformidade.
