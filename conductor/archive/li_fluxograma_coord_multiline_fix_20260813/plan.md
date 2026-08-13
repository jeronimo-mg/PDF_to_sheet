# Implementation Plan: Correção de Mesclagem Multi-linha para Coordenadas e Fluxogramas na Coluna FLUXOGRAMA/COORD

Fix coordinate truncation bug in `cleaner.py` and verify `FLUXOGRAMA / COORD.` multiline formatting in `LI_output.xlsx`.

## Proposed Phased Development

### Phase 1: Dynamic Multi-Line Continuation Implementation
- [x] Task: Dynamic Multi-Line Continuation in cleaner.py
    - [x] Write unit tests in `tests/test_coord_multiline.py` verifying coordinate linebreak concatenation.
    - [x] Update `merge_adjacent_item_rows` in `src/pdf_to_sheet/cleaner.py` to concatenate non-duplicate text values dynamically.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Dynamic Multi-Line Continuation Implementation' (Protocol in workflow.md)

### Phase 2: End-to-End Verification & Code Quality Gates
- [x] Task: Empirical Re-conversion & Code Quality Gates
    - [x] Re-convert `R11.01-2151-LI-0001_3-1.pdf` -> `LI_output.xlsx` and verify `G-5`, `G-6`, `D-7` coordinates in Excel.
    - [x] Run static analysis (`ruff check .`, `mypy src`) and full test suite (`pytest`) ensuring clean pass.
- [x] Task: Conductor - User Manual Verification 'Phase 2: End-to-End Verification & Code Quality Gates' (Protocol in workflow.md)
