# APU do NES

## Canais

- pulse 1 e pulse 2 com duty, envelope e sweep;
- triangle com linear counter;
- noise com LFSR de 15 bits;
- DMC com endereço, tamanho, loop, output level e IRQ.

## Frame sequencer

Os modos de quatro e cinco passos clockam envelopes, length counters, sweep e linear counter. O modo de quatro passos pode gerar frame IRQ.

## Áudio headless

O mixer produz amostras unsigned de 8 bits em um ring buffer de 65.536 bytes. A saída é determinística e pode ser comparada por SHA-256 entre VM e C11.
