# Track Specification: Correção de Alinhamento de Colunas (SISTEMA / INSTRUM.) e Separação de Sub-cabeçalhos em Tabelas LI

## 1. Overview
- **Track ID:** `li_header_alignment_fix_20260813`
- **Type:** Bug Fix
- **Goal:** Fix column misalignment and sub-header cell corruption in Instrument List (LI) documents (e.g., `R11.01-2151-LI-0001_3-1.pdf`), ensuring sub-header labels (`SISTEMA`, `INSTRUM.`, `MEC`, `ELE`) are properly separated from data values (`TE-1501`, `CS-1`, `N1E`, `2151`) into distinct header rows and data cells.

## 2. Functional Requirements
1. **Sub-Header Text Separation (`src/pdf_to_sheet/cleaner.py`):**
   - Implement `separate_subheaders_from_data` to detect when sub-header keywords (`SISTEMA`, `INSTRUM.`, `MEC`, `ELE`) are grouped into the same row as initial data values (`TE-1501`, `CS-1`, `N1E`, `2151`).
   - Split mixed header/data rows into two distinct rows:
     - Header Row: Contains `SISTEMA`, `INSTRUM.`, `MEC`, `ELE`.
     - Data Row 1: Contains `2151`, `TE-1501`, `CS-1`, `N1E`.
2. **Column Alignment Verification:**
   - Ensure Column B (`SISTEMA`) consistently contains system codes (e.g. `2151`).
   - Ensure Column C (`INSTRUM.`) consistently contains instrument TAGs (e.g. `TE-1501`, `TT-1501`, `TI-1501`, `HV-1505`).
3. **Local AI Vision Fallback Support:**
   - Enable local AI vision fallback if text-based header boundary extraction produces ambiguous column alignments.

## 3. Non-Functional Requirements & Quality Criteria
- **Regression Prevention:** All existing LE table extraction tests must remain passing.
- **Unit Testing:** Unit tests verifying LI header separation and column alignment in `tests/test_li_alignment.py`.
- **Static Analysis & Testing:** 100% pass on `pytest`, `ruff check .`, and `mypy src`.
