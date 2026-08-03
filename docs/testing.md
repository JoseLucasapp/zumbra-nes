# Testes Z21

As fixtures são sintéticas e não contêm conteúdo comercial.

## Totais

- 10 testes herdados da Z19;
- 13 testes de CPU da Z20;
- 20 testes de hardware da Z21;
- **43 testes totais**.

## Novos testes Z21

### PPU

- `ppu_memory_test.zum`;
- `ppu_register_test.zum`;
- `ppu_vblank_nmi_test.zum`;
- `ppu_background_test.zum`;
- `ppu_scroll_test.zum`;
- `ppu_sprite_test.zum`;
- `ppu_sprite_overflow_test.zum`;
- `ppu_frame_test.zum`.

### APU

- `apu_register_test.zum`;
- `apu_pulse_test.zum`;
- `apu_triangle_test.zum`;
- `apu_noise_test.zum`;
- `apu_dmc_test.zum`;
- `apu_frame_irq_test.zum`;
- `apu_audio_test.zum`.

### I/O e integração

- `controller_test.zum`;
- `dma_test.zum`;
- `console_sync_test.zum`;
- `console_dma_test.zum`;
- `console_nmi_test.zum`.

## Gate

```bash
EXPECTED_ZUMBRA_VERSION=0.14.2 scripts/test-z21-hardware.sh
```

O gate valida os 43 testes pela VM e valida o programa completo pelo backend C11. `metadata_test.zum` usa `createFile` e permanece coberto pela VM; os demais testes podem ser compilados individualmente pelo backend nativo.
