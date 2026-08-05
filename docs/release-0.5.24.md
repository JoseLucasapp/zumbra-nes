# Zumbra NES 0.5.25

Correção focada no build desktop nativo após a 0.5.23.

## Correção

O comando:

```bash
zumbra app build --manifest zumbra-app.toml --target linux --arch amd64 --release -o build/zumbra-nes
```

falia com:

```text
types: function has conflicting return types: null and bool
```

A 0.5.25 remove retornos implícitos conflitantes no frontend desktop e no bridge nativo, tornando explícitos os retornos dos helpers usados pelo pipeline de aplicação.

## Critério de aprovação

```text
Zumbra NES Z23 compatibility
0.5.25
Built release desktop application: /home/joselucasapp/projects/zumbra-nes/build/zumbra-nes
Z23 compatibility, persistence and debugger gate passed.
```
