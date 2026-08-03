# Arquitetura Z20

## Camadas

### `src/core`

Código determinístico e independente da interface:

- `header.zum`: valida e interpreta iNES/NES 2.0;
- `cartridge.zum`: separa trainer, PRG e CHR;
- `mapper.zum`: contrato de mapeamento e Mapper 0;
- `bus.zum`: mapa de memória visto pela CPU;
- `cpu6502.zum`: CPU Ricoh 2A03/NMOS 6502;
- `clock.zum`: scheduler 3 PPU : 1 CPU;
- `devices.zum`: contratos para PPU, APU, controles e linhas de CPU.

### `src/frontend`

- `headless.zum`: executa duas instruções e produz diagnóstico reproduzível;
- `desktop_contract.zum`: fronteira neutra para o frontend SDL futuro.

### `src/persistence`

- `metadata.zum`: grava metadados e hashes sem copiar a ROM.

### `src/testing`

- `assert.zum`: asserts portáveis entre VM e C11;
- `cpu_fixture.zum`: máquina NROM sintética, instalação de programas e vetores.

## Fluxo de execução

```text
arquivo .nes
    ↓
header.inspect
    ↓
cartridge.load
    ↓
Mapper 0 + Bus
    ↓
cpu6502.create → reset vector
    ↓
fetch → decode → execute
    ↓
clock.stepCpu(ciclos)
    ↓
frontend headless
```

## Estado da CPU

A CPU guarda:

```text
A, X, Y
SP, PC
status
cycles
instructions
lastOpcode
halted
irqLine
nmiPending
```

O status mantém o bit `U` ativo. O bit `B` não representa um latch físico: ele é aplicado somente nos valores empilhados por `BRK`/`PHP` e removido nos estados restaurados.

## Interrupções

Prioridade por fronteira de instrução:

1. NMI pendente;
2. IRQ ativa quando `I = 0`;
3. fetch da próxima instrução.

NMI e IRQ empilham PC e status com `B = 0`, ativam `I` e carregam seus vetores. BRK avança o PC de acordo com o byte de padding, empilha status com `B = 1` e usa o vetor IRQ/BRK.

## Ciclos

Cada `step` retorna os ciclos consumidos. O scheduler da Z19 recebe esse número e avança a PPU contratual em três ciclos por ciclo de CPU.

A Z20 contabiliza:

- ciclos-base por opcode;
- um ciclo adicional em leituras indexadas que cruzam página;
- um ciclo por branch tomado;
- mais um ciclo quando o branch tomado cruza página;
- sete ciclos em reset, IRQ e NMI.

## Fronteiras da Z20

A CPU está em nível de instrução e ciclos agregados. A Z20 não modela acessos internos a cada ciclo nem DMA de sprite, pois a PPU/APU ainda não existem.

Ficam fora deste marco:

- Z21: PPU, APU, controllers, DMA e sincronização de hardware;
- Z22: janela jogável, vídeo, áudio, seleção de ROM e conquistas locais;
- Z23: contas e sincronização online.
