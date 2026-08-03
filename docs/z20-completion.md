# Conclusão da Z20

## Definição de pronto

A Z20 está concluída quando:

- os 151 opcodes oficiais têm metadata e decoder;
- todos os modos de endereçamento oficiais funcionam;
- registradores, flags, stack e vetores são determinísticos;
- reset, NMI, IRQ, BRK e RTI passam nos testes;
- ciclos-base e penalidades passam nos testes;
- o smoke headless executa instruções reais;
- os 23 testes passam pela CLI oficial;
- o projeto compila pelo backend C11;
- o executável nativo roda;
- VM e nativo produzem saída idêntica;
- a higiene rejeita ROMs não permitidas e artefatos gerados.

## Critério automatizado

```bash
EXPECTED_ZUMBRA_VERSION=0.14.2 scripts/test-z20-cpu.sh
```

Resultado obrigatório:

```text
Zumbra NES repository hygiene checks passed.
Z20 CPU 6502 gate passed.
```

## Não pertencem à Z20

- PPU e frames;
- APU e áudio;
- controllers reais;
- OAM DMA;
- janela desktop jogável;
- conquistas;
- contas e sincronização.

Esses itens não devem ser usados para reabrir a Z20. A integração de hardware começa na Z21.
