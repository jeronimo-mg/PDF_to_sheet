# Track Specification: Formatagem Multi-linha e Mesclagem de Células para SERVIÇO, FLUXOGRAMA e FOLHA DE DADOS em Tabelas LI

## 1. Overview
- **Track ID:** `li_multiline_cell_formatting_20260813`
- **Type:** Feature
- **Goal:** Format 2-line fields (`SERVIÇO / LINHA`, `FLUXOGRAMA / COORD.`, `FOLHA DE DADOS / REQUISIÇÃO`) in Instrument List (LI) documents with clean vertical linebreaks (`\n`) so that sub-line 1 (description/drawing) and sub-line 2 (equipment tag/coordinate) display on two stacked lines inside Excel cells, preserving the original PDF visual structure.

## 2. Functional Requirements
1. **Vertical Linebreak Preservation in Sub-rows (`src/pdf_to_sheet/cleaner.py`):**
   - In `merge_adjacent_item_rows`, combine continuation text for multi-line description columns (columns `SERVIÇO`, `FLUXOGRAMA`, `FOLHA DE DADOS`) using `\n` instead of space `" "`.
   - Ensure clean whitespace normalization around `\n`.
2. **Excel Multi-line Layout Formatting (`src/pdf_to_sheet/writers/excel.py`):**
   - Ensure `wrap_text=True` renders linebreaks as stacked lines in Excel.
   - Set top vertical alignment (`vertical="top"`) so single-line cells align seamlessly with 2-line cells.

## 3. Non-Functional Requirements & Quality Criteria
- **Regression Prevention:** LE technical data table formatting must remain unaffected.
- **Unit Testing:** Unit tests verifying `\n` linebreak preservation in `tests/test_multiline_formatting.py`.
- **Static Analysis & Testing:** 100% pass on `pytest`, `ruff check .`, and `mypy src`.
