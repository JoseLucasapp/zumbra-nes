# Suporte iNES no Z19

## iNES 1.0

O parser lê:

- quantidade de bancos PRG/CHR;
- mapper de 8 bits;
- mirroring horizontal, vertical ou four-screen;
- bateria;
- trainer;
- tipo de console;
- PRG RAM declarada no byte 8.

## NES 2.0

O Z19 identifica NES 2.0 pelo campo `flags7 & 0x0C == 0x08` e lê:

- mapper de 12 bits;
- submapper;
- tamanhos lineares de PRG e CHR;
- RAM/NVRAM pelas codificações de shift;
- timing mode.

A codificação exponencial/multiplicadora de tamanho é rejeitada com uma mensagem explícita e será implementada junto da expansão de formatos no Z20.

## Mapper 0

- NROM-128: PRG de 16 KiB espelhado em `$8000-$FFFF`;
- NROM-256: PRG de 32 KiB linear em `$8000-$FFFF`;
- CHR ROM de 8 KiB ou CHR RAM de 8 KiB;
- PRG RAM de 8 KiB em `$6000-$7FFF`.
