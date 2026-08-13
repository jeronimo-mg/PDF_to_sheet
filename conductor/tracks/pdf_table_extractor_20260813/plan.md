# Implementation Plan: Develop PDF to XLSX Table Extractor CLI with Hybrid Local Parsing

Develop a high-accuracy, privacy-focused Python CLI utility that parses complex engineering tables from PDF documents (such as technical lists LE/LI) and exports them into structured Excel (`.xlsx`) files using rule-based parsing with local AI vision fallback.

## User Review Required

> [!IMPORTANT]
> Empirical validation requires test executions on sample PDFs (`R11.01-2151-LE-0001_2.pdf` and `R11.01-2151-LI-0001_3-1.pdf`). Ensure local Python 3.10+ runtime and optional Ollama AI service are accessible.

## Proposed Phased Development

### Phase 1: Project Setup & Core Data Models
- [ ] Task: Environment & Dependency Configuration
    - [ ] Write dependency files (`requirements.txt` / `pyproject.toml`) and establish project directory layout (`src/pdf_to_sheet/`, `tests/`).
    - [ ] Configure `pytest`, `ruff`, and `mypy` settings.
- [ ] Task: Unified Data Models & Interface Definition
    - [ ] Write unit tests for core data models (`Cell`, `TableData`, `ExtractionResult`) in `tests/test_models.py`.
    - [ ] Implement data models and abstract `BaseExtractor` interface in `src/pdf_to_sheet/models.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Project Setup & Core Data Models' (Protocol in workflow.md)

### Phase 2: Rule-Based PDF Table Extractor Engine
- [ ] Task: Rule-Based Extractor (pdfplumber / camelot)
    - [ ] Write unit tests for deterministic PDF table parsing in `tests/test_rule_extractor.py`.
    - [ ] Implement `RuleBasedExtractor` using `pdfplumber` and `camelot` in `src/pdf_to_sheet/extractors/rule_based.py`.
- [ ] Task: Multi-page Table Assembly & Header Merging
    - [ ] Write unit tests for multi-page header detection and continuous row concatenation in `tests/test_table_merger.py`.
    - [ ] Implement table merging logic in `src/pdf_to_sheet/merger.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Rule-Based PDF Table Extractor Engine' (Protocol in workflow.md)

### Phase 3: Local AI Vision Fallback Integration
- [ ] Task: Ollama Local Service Detector & Image Preprocessor
    - [ ] Write unit tests for Ollama status checking and page image rendering in `tests/test_local_ai.py`.
    - [ ] Implement local AI health check and PDF page-to-image rendering in `src/pdf_to_sheet/extractors/local_ai.py`.
- [ ] Task: Local AI Vision Table Extraction Strategy
    - [ ] Write unit tests for hybrid fallback orchestration in `tests/test_fallback.py`.
    - [ ] Implement `HybridTableExtractor` combining rule-based and local AI vision parsing in `src/pdf_to_sheet/extractors/hybrid.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Local AI Vision Fallback Integration' (Protocol in workflow.md)

### Phase 4: Excel (.xlsx) Exporter & Formatting Engine
- [ ] Task: Data Typing & OpenPyXL Excel Builder
    - [ ] Write unit tests for Excel formatting, data type inference, confidence highlights, and multi-sheet generation in `tests/test_excel_writer.py`.
    - [ ] Implement `ExcelWriter` using `pandas` and `openpyxl` in `src/pdf_to_sheet/writers/excel.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Excel (.xlsx) Exporter & Formatting Engine' (Protocol in workflow.md)

### Phase 5: CLI Interface, Verification & Delivery
- [ ] Task: Click/Rich CLI Application
    - [ ] Write CLI tests for `--file` and `--dir` argument handling in `tests/test_cli.py`.
    - [ ] Implement CLI entrypoint with Rich progress bars and audit logging in `src/pdf_to_sheet/cli.py`.
- [ ] Task: End-to-End Empirical Validation & Quality Verification
    - [ ] Perform empirical conversion runs on `R11.01-2151-LE-0001_2.pdf` and `R11.01-2151-LI-0001_3-1.pdf`.
    - [ ] Run static analysis (`ruff check .`, `mypy .`) and test suite (`pytest`) ensuring clean pass.
- [ ] Task: Conductor - User Manual Verification 'Phase 5: CLI Interface, Verification & Delivery' (Protocol in workflow.md)
