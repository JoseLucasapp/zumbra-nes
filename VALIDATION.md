# Validation report — Z19 foundation 0.1.0

## Executed in the delivery environment

- all 22 `.zum` files parsed successfully;
- canonical Zumbra front-end pipeline completed for every source and test file:
  - parser;
  - module resolution;
  - semantic analysis;
  - type checking;
  - HIR;
  - MIR;
  - MIR optimization;
- official formatter applied to all `.zum` files;
- official linter passed with the same non-pipeline options used by the gate;
- synthetic fixture SHA-256 checks passed;
- repository hygiene passed;
- shell scripts passed `bash -n`;
- fixture generator passed Python compilation;
- GitHub Actions workflow passed YAML parsing.

## Not executable in the delivery environment

The complete `scripts/test-z19-foundation.sh` gate requires the published Zumbra 0.14.1 CLI and its native build dependencies. The delivery environment did not contain that binary and could not download external dependencies.

Run on the target development machine:

```bash
EXPECTED_ZUMBRA_VERSION=0.14.1 scripts/test-z19-foundation.sh
```

For a first interpreted-only validation:

```bash
Z19_SKIP_NATIVE=1 EXPECTED_ZUMBRA_VERSION=0.14.1 scripts/test-z19-foundation.sh
```

## Approval criteria

The foundation is approved when the complete gate ends with:

```text
Z19 repository hygiene checks passed.
Z19 foundation gate passed.
```
