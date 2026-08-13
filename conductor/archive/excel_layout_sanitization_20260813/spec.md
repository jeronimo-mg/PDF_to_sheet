# Track Specification: Saneamento de Artefatos em Células, Alinhamento de TAGs e Largura com Quebra no Excel

## 1. Overview
- **Track ID:** `excel_layout_sanitization_20260813`
- **Type:** Bug Fix / Refactoring
- **Goal:** Fix column width explosion, text overflow, corrupted cell 0 (`Rev.`) artifacts, and un-linked equipment sub-rows (`CASCO`) in Excel exports (`LE_output.xlsx` and `LI_output.xlsx`).

## 2. Functional Requirements
1. **Cell 0 (`Rev.`) Artifact Sanitization:**
   - Detect corrupted cell 0 entries (containing > 10 characters or multi-column text strings from overlapping PDF bounding boxes).
   - Sanitize corrupted cell 0 entries back to valid revision numbers (`1`).
2. **Secondary Row TAG Alignment & Propagation:**
   - Detect sub-rows with missing TAGs (e.g. `(CASCO)` or `(TUBOS)`).
   - Propagate parent TAG to sub-rows (e.g., `2151-TC01 (CASCO)`).
3. **OpenPyXL Excel Layout & Dimension Controls:**
   - Cap maximum column width to **45 characters max** (and minimum 10 characters).
   - Enable text wrapping (`wrap_text=True`) and top vertical alignment (`vertical='top'`) for all data cells.
   - Remove empty trailing columns without header titles.

## 3. Non-Functional Requirements & Quality Criteria
- **Visual & Empirical Verification:** Clean, readable Excel spreadsheets for `LE_output.xlsx` and `LI_output.xlsx` with zero horizontal screen overflow.
- **Unit Testing:** Tests covering artifact sanitization, TAG propagation, and Excel column formatting in `tests/`.
- **Static Analysis:** Zero errors on `ruff check .` and `mypy src`.
