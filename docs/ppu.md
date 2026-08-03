# PPU Ricoh 2C02

## Registradores

- `$2000` PPUCTRL;
- `$2001` PPUMASK;
- `$2002` PPUSTATUS;
- `$2003` OAMADDR;
- `$2004` OAMDATA;
- `$2005` PPUSCROLL;
- `$2006` PPUADDR;
- `$2007` PPUDATA.

O bus espelha esses registradores até `$3FFF`.

## Memória

- `$0000-$1FFF`: CHR pelo mapper;
- `$2000-$3EFF`: nametables e mirrors;
- `$3F00-$3FFF`: palette RAM de 32 bytes com mirrors especiais.

## Render

O framebuffer contém 61.440 índices de paleta. Background usa tile, attribute table e pattern bits. Sprites suportam tamanhos 8×8 e 8×16, flip, prioridade, sprite zero hit e overflow de oito sprites por scanline.

## Timing

A PPU avança por dot e scanline, gera VBlank/NMI e aplica o skip de um dot em frame ímpar quando rendering está ativo.
