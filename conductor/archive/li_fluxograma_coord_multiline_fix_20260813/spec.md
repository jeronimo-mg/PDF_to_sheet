# Track Specification: Correção de Mesclagem Multi-linha para Coordenadas e Fluxogramas na Coluna FLUXOGRAMA/COORD

## 1. Overview
- **Track ID:** `li_fluxograma_coord_multiline_fix_20260813`
- **Type:** Bug Fix
- **Goal:** Fix coordinate truncation in the `FLUXOGRAMA / COORD.` column in Instrument List (LI) documents (e.g. `R11.01-2151-LI-0001_3-1.pdf`), ensuring sub-line 2 coordinates (e.g. `G-5`, `G-6`, `D-7`) are preserved and displayed on a stacked second line (`\n`) below the drawing number (`R11.01-2151-XE-0001`).

## 2. Functional Requirements
1. **Dynamic Column Multi-line Continuation (`src/pdf_to_sheet/cleaner.py`):**
   - Update `merge_adjacent_item_rows` to remove hardcoded column index boundaries (`col_idx >= num_cols - 2`).
   - For all non-empty cell continuation values (`val_next`) that differ from `val_curr`, concatenate them with `\n` if not already present.
2. **Coordinate Preservation Verification:**
   - Verify that `FLUXOGRAMA / COORD.` cells contain both the drawing number and coordinate stacked on 2 lines (e.g., `R11.01-2151-XE-0001\nG-5`).

## 3. Non-Functional Requirements & Quality Criteria
- **Regression Prevention:** All existing LE and LI extraction unit tests must remain passing.
- **Unit Testing:** Unit tests verifying coordinate multiline merging in `tests/test_coord_multiline.py`.
- **Static Analysis & Testing:** 100% pass on `pytest`, `ruff check .`, and `mypy src`.
