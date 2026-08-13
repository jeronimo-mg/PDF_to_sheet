# Implementation Plan: Saneamento de Artefatos em Células, Alinhamento de TAGs e Largura com Quebra no Excel

Sanitize corrupted cell 0 text artifacts, align sub-row TAGs, enforce capped column widths with text wrapping, and clean up empty trailing columns in Excel exports.

## Proposed Phased Development

### Phase 1: Cell Artifact Sanitizer & Sub-Row TAG Alignment Engine
- [x] Task: Row Sanitizer & TAG Propagation Module
    - [x] Write unit tests for cell 0 artifact sanitization and sub-row TAG propagation in `tests/test_row_sanitizer.py`.
    - [x] Implement `sanitize_table_rows` in `src/pdf_to_sheet/cleaner.py` and integrate into `src/pdf_to_sheet/extractors/rule_based.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Cell Artifact Sanitizer & Sub-Row TAG Alignment Engine' (Protocol in workflow.md)

### Phase 2: Excel Layout & Column Dimension Controls
- [x] Task: OpenPyXL Width Capping & Text Wrapping Formatting
    - [x] Write unit tests for max width capping and text wrapping formatting in `tests/test_excel_formatting.py`.
    - [x] Update `ExcelWriter` in `src/pdf_to_sheet/writers/excel.py` to enforce width bounds (10 to 45), apply `wrap_text=True` and `vertical='top'`, and drop empty trailing columns.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Excel Layout & Column Dimension Controls' (Protocol in workflow.md)

### Phase 3: End-to-End Empirical Verification & Code Quality Gates
- [x] Task: Empirical Re-conversion & Code Quality Gates
    - [x] Re-run conversion on `R11.01-2151-LE-0001_2.pdf` -> `LE_output.xlsx` and `R11.01-2151-LI-0001_3-1.pdf` -> `LI_output.xlsx` and verify Excel dimensions.
    - [x] Run static analysis (`ruff check .`, `mypy src`) and full test suite (`pytest`) ensuring clean pass.
- [x] Task: Conductor - User Manual Verification 'Phase 3: End-to-End Empirical Verification & Code Quality Gates' (Protocol in workflow.md)
