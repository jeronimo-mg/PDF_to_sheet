# Implementation Plan: Correção de Alinhamento de Colunas (SISTEMA / INSTRUM.) e Separação de Sub-cabeçalhos em Tabelas LI

Fix LI sub-header grouping bug in `cleaner.py` and verify column alignments in `LI_output.xlsx`.

## Proposed Phased Development

### Phase 1: LI Sub-Header & Data Row Separator Implementation
- [x] Task: Sub-Header Row Splitter in cleaner.py
    - [x] Write unit tests in `tests/test_li_alignment.py` verifying sub-header text separation.
    - [x] Implement `split_mixed_header_data_rows` in `src/pdf_to_sheet/cleaner.py` to decouple header keywords (`SISTEMA`, `INSTRUM.`, `MEC`, `ELE`) from data values.
- [x] Task: Conductor - User Manual Verification 'Phase 1: LI Sub-Header & Data Row Separator Implementation' (Protocol in workflow.md)

### Phase 2: End-to-End Verification & Code Quality Gates
- [x] Task: Empirical Re-conversion & Code Quality Gates
    - [x] Re-convert `R11.01-2151-LI-0001_3-1.pdf` -> `LI_output.xlsx` and verify `SISTEMA` and `INSTRUM.` columns.
    - [x] Run static analysis (`ruff check .`, `mypy src`) and full test suite (`pytest`) ensuring clean pass.
- [x] Task: Conductor - User Manual Verification 'Phase 2: End-to-End Verification & Code Quality Gates' (Protocol in workflow.md)
