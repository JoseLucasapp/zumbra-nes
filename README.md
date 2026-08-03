# Zumbra NES

Emulador NES/Famicom em desenvolvimento, escrito em **Zumbra 0.14.2**.

A versão `0.3.0` conclui o marco **Z21**: PPU, APU, controles, OAM DMA e o scheduler completo de CPU/PPU/APU foram integrados ao núcleo criado nas Z19 e Z20. O projeto permanece headless nesta versão; janela, teclado/gamepad real, conquistas e persistência do usuário pertencem à Z22.

## Implementado

### Z19 — fundação

- parser iNES 1.0 e identificação básica de NES 2.0;
- cartucho, trainer, PRG ROM/RAM e CHR ROM/RAM;
- Mapper 0 com NROM-128 e NROM-256;
- barramento inicial, vetores e fixtures sintéticas.

### Z20 — CPU 6502

- CPU Ricoh 2A03/NMOS 6502;
- 151 opcodes oficiais;
- todos os modos oficiais de endereçamento;
- stack, flags, reset, IRQ, NMI, BRK e ciclos agregados;
- page crossing e bug do `JMP ($xxFF)`.

### Z21 — hardware do NES

- PPU Ricoh 2C02 com `PPUCTRL`, `PPUMASK`, `PPUSTATUS`, OAM, scroll, endereço e dados;
- pattern tables, nametables, attribute tables, palette RAM e mirroring horizontal/vertical/four-screen;
- framebuffer determinístico de `256×240` índices de paleta;
- background, sprites 8×8/8×16, prioridade, flip, sprite zero hit e overflow;
- scanlines, dots, VBlank, NMI e odd-frame cycle skip;
- OAM DMA por `$4014`, com 513/514 ciclos de stall;
- dois controles em `$4016/$4017`, strobe e leitura serial A/B/Select/Start/direções;
- APU com pulse 1/2, triangle, noise e DMC;
- envelopes, sweep, length counters, linear counter, LFSR, frame counter e IRQs;
- buffer PCM determinístico e digest SHA-256;
- scheduler central com razão `3 PPU : 1 CPU : 1 APU`;
- propagação PPU NMI, APU IRQ, DMA e fetch do DMC;
- paridade de saída entre VM e executável C11.

## Requisitos

- Zumbra `0.14.2` no `PATH`;
- Linux para o gate nativo oficial atual;
- `clang` ou `gcc`;
- dependências nativas exigidas pela distribuição da Zumbra.

```bash
zumbra --version
```

Resultado esperado:

```text
0.14.2
```

## Testes

```bash
zumbra project check
zumbra project test
zumbra project run
```

Gate oficial da Z21:

```bash
scripts/test-z21-hardware.sh
```

O gate executa hashes das fixtures, verificação dos 151 opcodes, formatter, linter, pipeline, **43 testes**, documentação, VM, build C11, execução nativa, paridade VM/native e higiene.

Para diagnóstico sem o build nativo, sem substituir a aprovação oficial:

```bash
Z21_SKIP_NATIVE=1 scripts/test-z21-hardware.sh
```

Os gates históricos encaminham para o gate atual. As árvores originais permanecem preservadas nas tags `v0.1.0` e `v0.2.0`.

## Saída headless

O programa principal carrega uma fixture NROM sintética, executa duas instruções da CPU, configura pulse e controle, avança um frame de hardware e imprime estado estável:

```text
Zumbra NES Z21 hardware
CPU A = 1
CPU instructions = 2
PPU frame = 1
controller A = 1
frame/audio SHA-256
```

## ROMs

O repositório aceita somente ROMs sintéticas, homebrew com redistribuição permitida ou dumps produzidos legalmente pelo próprio usuário. Nenhuma ROM comercial é incluída.

## Estado

- Z19: publicada como `v0.1.0`;
- Z20: publicada como `v0.2.0`;
- Z21: hardware headless completo no escopo da versão `0.3.0`;
- próximo marco: Z22, com frontend desktop jogável, input real, seleção de ROM e conquistas locais em SQLite.

Documentação técnica: [`docs/ppu.md`](docs/ppu.md), [`docs/apu.md`](docs/apu.md), [`docs/architecture.md`](docs/architecture.md) e [`docs/z21-completion.md`](docs/z21-completion.md).
