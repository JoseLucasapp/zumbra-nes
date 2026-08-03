# Conclusão da Z21

A Z21 está concluída quando:

- PPU, APU, controles e DMA passam nos testes;
- CPU/PPU/APU mantêm a razão de clock esperada;
- VBlank/NMI e APU IRQ chegam à CPU;
- um frame e áudio headless são determinísticos;
- os 43 testes passam;
- o executável C11 é gerado e executado;
- VM e nativo produzem o mesmo relatório;
- a higiene passa.

Comando canônico:

```bash
EXPECTED_ZUMBRA_VERSION=0.14.2 scripts/test-z21-hardware.sh
```

Próximo marco: Z22, frontend jogável e conquistas locais em SQLite.
