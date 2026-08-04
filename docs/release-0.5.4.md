# Zumbra NES 0.5.4 — Mapper 227 visible-idle hotfix

Hotfix sobre 0.5.4.

A 0.5.4 compilava e empacotava corretamente, mas o throttle de idle do Mapper 227 podia entrar depois do primeiro frame ainda cinza. Em ROMs reais como `1200-in-1.nes`, isso podia congelar visualmente a tela antes do menu terminar de desenhar.

## Correção

- o idle do Mapper 227 agora só ativa depois de pelo menos 60 frames;
- o idle também exige detecção de frame visível/variado;
- frames totalmente cinza, pretos ou uniformes não ativam o modo idle;
- o binário continua usando Zumbra 0.14.3.

## Validação esperada

```bash
EXPECTED_ZUMBRA_VERSION=0.14.3 scripts/test-z23-compatibility.sh
./build/zumbra-nes "$HOME/Downloads/1200-in-1.nes"
```

Esperado: o gate passa, o binário é criado e a ROM real recebe tempo de CPU suficiente para sair da tela inicial cinza antes do throttle.
