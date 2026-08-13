# Track Specification: Atalho de Duplo Clique com Janela de Seleção Visual para Conversão PDF para Excel

## 1. Overview
- **Track ID:** `gui_double_click_shortcut_20260813`
- **Type:** Feature
- **Goal:** Provide a zero-friction double-clickable Windows shortcut (`Converter_PDF_para_Excel.bat`) and native file dialog GUI picker in `cli.py` to allow users to select any PDF with a single click, convert it to `.xlsx`, and automatically open the resulting Excel spreadsheet.

## 2. Functional Requirements
1. **Windows Double-Click Launcher (`Converter_PDF_para_Excel.bat`):**
   - Create a clean Windows batch file that launches `python -m pdf_to_sheet.cli --gui`.
   - Support drag-and-drop: dropping a `.pdf` directly onto the `.bat` icon instantly converts it.
2. **Native Windows File Picker & Auto-Open (`src/pdf_to_sheet/cli.py`):**
   - Add `--gui` option to `cli.py`.
   - If `--gui` is set (or no arguments provided), launch native Windows file dialog (`tkinter.filedialog.askopenfilename`).
   - After successful conversion, auto-open the generated `.xlsx` workbook on Windows using `os.startfile`.
3. **Robust Fallbacks & Error Handling:**
   - Handle user cancellation in file picker cleanly without throwing exceptions.
   - Display Rich progress and clear success messages.

## 3. Non-Functional Requirements & Quality Criteria
- **Ease of Use:** Zero terminal typing required for end-users.
- **Unit Testing:** Unit tests verifying CLI `--gui` option handling and batch launcher compatibility.
- **Static Analysis:** 100% pass on `pytest`, `ruff check .`, and `mypy src`.
