# Zumbra NES 0.5.5 — startup, Mapper 227 input and safe audio hotfix

Hotfix sobre 0.5.4.

A 0.5.4 abre a ROM Mapper 227 real, mas ainda exibe a superfície inicial do SDL/compositor antes da primeira imagem útil da ROM, podendo aparecer como janela transparente e depois cinza. Também mantém áudio experimental ativo no Mapper 227 e fatias pequenas demais durante input, causando som ruim e resposta lenta.

A 0.5.5 corrige esse fluxo sem alterar a Zumbra-lang, que permanece em 0.14.3.

## Mudanças

- adiciona splash/intro nativa do emulador antes da primeira imagem útil da ROM;
- mantém o splash enquanto o framebuffer da ROM ainda é cinza/uniforme;
- aumenta a fatia cooperativa do Mapper 227 de 96 para 1024 instruções;
- aumenta a fatia temporária com input para 16384 instruções;
- desativa a fila de áudio para Mapper 227 até o APU/timing real ser refinado;
- mantém o throttle de idle para reduzir CPU quando o menu está parado;
- preserva os aliases de teclado da 0.5.4.

## Controles

```text
Select: Right Shift, Left Shift, Tab ou Backspace
Start:  Enter, Space ou Enter numérico
Mover:  setas ou WASD
A/B:    Z/X ou J/K
Esc:    fechar
```

## Validação

```text
format: 110 file(s), 0 changed
lint: 0 error(s), 0 warning(s), 0 info(s)
project test: 75 test file(s) executed
native headless build: OK
VM/native diff: vazio
app build desktop release: OK
```

O gate integral com empacotamento deve ser executado no Debian do usuário antes de publicar a release.
