# Save RAM e save states Z23

## SRAM

- somente cartuchos com battery flag;
- arquivo por SHA-256 da ROM;
- caminho `saves/<digest>.sav`;
- dirty flag no bus;
- carregamento na abertura;
- flush periódico e no fechamento.

## Save states

Formato atual:

```text
schema: 1
format: Z23-0.5.0
```

Conteúdo:

- CPU e interrupções;
- RAM, PRG RAM, APU I/O e open bus;
- mapper e registradores;
- PPU, VRAM, paleta, OAM e framebuffer;
- APU e ring buffer;
- controles;
- DMA, ciclos e frame.

A PRG ROM não é duplicada. A restauração é rejeitada quando schema, formato, digest ou mapper não coincidem.

O frontend possui slots `0`–`9`. As teclas numéricas selecionam o slot, `Q` salva e `E` restaura.
