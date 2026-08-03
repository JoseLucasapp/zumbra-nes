# Critérios de conclusão da Z19

## Implementação técnica

- [x] projeto separado do compilador Zumbra;
- [x] versão inicial `0.1.0`;
- [x] leitor binário e validação de limites;
- [x] parser iNES 1.0;
- [x] identificação NES 2.0;
- [x] estrutura `Cartridge`;
- [x] contrato de mapper;
- [x] Mapper 0/NROM;
- [x] barramento e mapa de memória da CPU;
- [x] contratos CPU/PPU/APU/controle;
- [x] relógio determinístico;
- [x] frontend headless;
- [x] persistência de metadados;
- [x] fixtures sintéticas;
- [x] dez testes automatizados;
- [x] documentação de arquitetura;
- [x] gate único da Z19;
- [x] suporte nativo a `panic` fornecido pela Zumbra 0.14.2;
- [x] build C11 nativo incluído no gate;
- [x] execução do binário nativo incluída no gate;
- [x] comparação entre saída VM e nativa incluída no gate.

## Publicação do repositório

O repositório remoto `JoseLucasapp/zumbra-nes` já existe. Restam ações externas ao código:

- [ ] executar o gate completo no ambiente do usuário com Zumbra 0.14.2;
- [ ] criar o commit inicial;
- [ ] enviar a branch `main`;
- [ ] criar e enviar a tag `v0.1.0`;
- [ ] confirmar o CI no GitHub Actions.

A Z20 só deve começar depois que essas validações externas forem confirmadas.
