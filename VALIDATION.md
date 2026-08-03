# Validation report — Z19 foundation 0.1.0

## Status

A implementação técnica da Z19 está concluída para Zumbra 0.14.2. O gate oficial exige a mesma saída na VM e no executável C11 nativo.

## Validações já comprovadas no ambiente do usuário

- hashes das seis fixtures sintéticas;
- formatter em 22 arquivos `.zum`;
- linter sem erros ou avisos bloqueantes;
- `zumbra project info`;
- `zumbra project check`;
- dez testes executáveis;
- documentação de 56 símbolos;
- execução headless pela VM;
- higiene do repositório.

## Correção de linguagem necessária para o fechamento

A Zumbra 0.14.2 adiciona suporte a `panic` no backend C11. A Z19 mantém validações defensivas e helpers de assert sem remover caminhos de erro para contornar o compilador.

## Gate oficial

```bash
EXPECTED_ZUMBRA_VERSION=0.14.2 scripts/test-z19-foundation.sh
```

O gate executa:

1. SHA-256 das fixtures;
2. formatter;
3. linter;
4. informações e análise do projeto;
5. dez testes;
6. geração da documentação;
7. execução pela VM;
8. build C11 nativo;
9. execução do binário nativo;
10. comparação exata entre as saídas VM e nativa;
11. higiene do repositório.

## Verificação rápida

```bash
Z19_SKIP_NATIVE=1 EXPECTED_ZUMBRA_VERSION=0.14.2 scripts/test-z19-foundation.sh
```

Esse modo não substitui o gate completo.

## Critérios de aprovação

```text
Z19 repository hygiene checks passed.
Z19 foundation gate passed.
```

Também devem existir:

```text
build/zumbra-nes
build/vm-smoke.txt
build/native-smoke.txt
```

E este comando deve retornar sucesso:

```bash
diff -u build/vm-smoke.txt build/native-smoke.txt
```
