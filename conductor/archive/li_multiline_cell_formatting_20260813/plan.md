# Implementation Plan: Formatagem Multi-linha e Mesclagem de Células para SERVIÇO, FLUXOGRAMA e FOLHA DE DADOS em Tabelas LI

Implement vertical linebreak `\n` preservation for LI 2-line fields and verify Excel workbook rendering.

## Proposed Phased Development

### Phase 1: Linebreak Preservation in Sub-Row Consolidation
- [x] Task: Linebreak Preservation in cleaner.py
    - [x] Write unit tests in `tests/test_multiline_formatting.py` verifying `\n` linebreaks for multi-line description fields.
    - [x] Update `merge_adjacent_item_rows` in `src/pdf_to_sheet/cleaner.py` to use `\n` for continuation text.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Linebreak Preservation in Sub-Row Consolidation' (Protocol in workflow.md)

### Phase 2: End-to-End Verification & Code Quality Gates
- [x] Task: Empirical Re-conversion & Code Quality Gates
    - [x] Re-convert `R11.01-2151-LI-0001_3-1.pdf` -> `LI_output.xlsx` and verify 2-line visual layout in Excel.
    - [x] Run static analysis (`ruff check .`, `mypy src`) and full test suite (`pytest`) ensuring clean pass.
- [x] Task: Conductor - User Manual Verification 'Phase 2: End-to-End Verification & Code Quality Gates' (Protocol in workflow.md)
