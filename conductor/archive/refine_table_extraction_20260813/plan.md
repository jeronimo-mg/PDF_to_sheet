# Implementation Plan: Refinar Extração de Tabelas LE/LI com Fusão de Cabeçalhos Multi-Linha e Filtro de Capa

Upgrade the PDF table extraction pipeline to filter cover page revision grids, merge 2-row table headers vertically, clean cell linebreaks, and produce clean Excel files for LE and LI documents.

## Proposed Phased Development

### Phase 1: Multi-Row Header Merging & Cell Cleaning Engine
- [x] Task: Multi-Row Header Merger & Text Cleaning Module
    - [x] Write unit tests for multi-row header merging and cell text cleaning in `tests/test_header_cleaner.py`.
    - [x] Implement `merge_multiline_headers` and cell line-break cleaner in `src/pdf_to_sheet/cleaner.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Multi-Row Header Merging & Cell Cleaning Engine' (Protocol in workflow.md)

### Phase 2: Table Classifier & Cover Page Filter
- [x] Task: Technical Table Classifier & Metadata Filter
    - [x] Write unit tests for table classification (data table vs revision/cover table) in `tests/test_table_filter.py`.
    - [x] Implement table classification logic in `src/pdf_to_sheet/extractors/rule_based.py` and `src/pdf_to_sheet/merger.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Table Classifier & Cover Page Filter' (Protocol in workflow.md)

### Phase 3: Excel Writer & Layout Refinement
- [x] Task: OpenPyXL Excel Formatting & Master Sheet Isolation
    - [x] Write unit tests for clean Excel sheet generation without cover metadata in `tests/test_excel_writer.py`.
    - [x] Update `ExcelWriter` in `src/pdf_to_sheet/writers/excel.py` to write clean headers, filter out footers, and format multi-sheet workbooks.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Excel Writer & Layout Refinement' (Protocol in workflow.md)

### Phase 4: End-to-End Empirical Validation & Quality Verification
- [x] Task: Empirical Conversion & Code Quality Gates
    - [x] Perform empirical conversion runs on `R11.01-2151-LE-0001_2.pdf` and `R11.01-2151-LI-0001_3-1.pdf` and inspect XLSX outputs.
    - [x] Run static analysis (`ruff check .`, `mypy src`) and full test suite (`pytest`) ensuring clean pass.
- [x] Task: Conductor - User Manual Verification 'Phase 4: End-to-End Empirical Validation & Quality Verification' (Protocol in workflow.md)
