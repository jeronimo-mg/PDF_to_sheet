# Track Specification: Develop PDF to XLSX Table Extractor CLI with Hybrid Local Parsing

## 1. Track Summary
- **Track ID:** `pdf_table_extractor_20260813`
- **Type:** Feature (Greenfield Core MVP)
- **Goal:** Develop a high-accuracy, privacy-focused Python CLI utility that parses complex tables from engineering PDF documents (specifically equipment lists LE/LI such as `R11.01-2151-LE-0001_2.pdf` and `R11.01-2151-LI-0001_3-1.pdf`) and exports them into structured Excel `.xlsx` spreadsheets.

## 2. Core Functional Requirements
1. **Rule-Based PDF Table Extraction (Tier 1):**
   - Extract tables using `pdfplumber` and `camelot`.
   - Reconstruct bounding boxes, multi-line headers, cell boundaries, and cell alignment.
2. **Local AI Model Fallback (Tier 2):**
   - Detect unruled, borderless, or low-confidence table extractions.
   - Automatically fallback to an offline local AI model (Ollama vision endpoint at `http://localhost:11434`) to extract tabular structures without remote cloud requests.
3. **Multi-Page & Multi-Sheet Excel Generator:**
   - Detect multi-page technical tables and merge split headers into unified datasets.
   - Export Excel workbooks featuring individual page/table sheets and a consolidated master worksheet.
   - Perform automatic data typing (integers, floats, dates, strings) and highlight low-confidence rows.
4. **Command-Line Interface:**
   - Provide CLI arguments (`--file` for single PDF, `--dir` for batch processing, `--output` for destination folder).
   - Display clean terminal progress bars (`rich` / `tqdm`) and generate execution logs (`.log`).

## 3. Technical Stack & Architecture
- **Language:** Python 3.10+
- **Parsing Libraries:** `pdfplumber`, `camelot-py`, `pypdfium2`, `pdf2image`, `Pillow`
- **Excel & Data Libraries:** `pandas`, `openpyxl`
- **Local AI Service:** Ollama Vision API (HTTP endpoint `http://localhost:11434`)
- **CLI & UX:** `click` / `typer`, `rich`
- **Quality & Testing:** `pytest`, `ruff`, `mypy`

## 4. Quality Gates & Acceptance Criteria
- **Unit & Integration Testing:** All unit tests pass with `pytest`.
- **Empirical Sample Validation:** Successfully convert `R11.01-2151-LE-0001_2.pdf` and `R11.01-2151-LI-0001_3-1.pdf` into `.xlsx` files with verified header structure and cell alignment.
- **Static Analysis:** `ruff check .` and `mypy .` pass cleanly with zero errors.
