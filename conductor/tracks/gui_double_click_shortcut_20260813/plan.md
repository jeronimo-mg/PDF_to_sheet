# Implementation Plan: Atalho de Duplo Clique com Janela de Seleção Visual para Conversão PDF para Excel

Implement native Windows file dialog integration in CLI, auto-open Excel functionality, and create the double-clickable `Converter_PDF_para_Excel.bat` script.

## Proposed Phased Development

### Phase 1: CLI Native File Picker & Auto-Open Feature
- [x] Task: CLI GUI Picker & Auto-Open Integration
    - [x] Write unit tests for CLI GUI flag handling in `tests/test_cli_gui.py`.
    - [x] Implement `--gui` option, `tkinter` file dialog picker, and `os.startfile` auto-open in `src/pdf_to_sheet/cli.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: CLI Native File Picker & Auto-Open Feature' (Protocol in workflow.md)

### Phase 2: Double-Click Batch Launcher & Shortcut Creation
- [x] Task: Windows Batch Launcher Script
    - [x] Create `Converter_PDF_para_Excel.bat` launcher script with drag-and-drop and double-click support.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Double-Click Batch Launcher & Shortcut Creation' (Protocol in workflow.md)

### Phase 3: End-to-End Verification & Code Quality Gates
- [x] Task: Quality Verification & Static Analysis
    - [x] Run static analysis (`ruff check .`, `mypy src`) and full test suite (`pytest`) ensuring clean pass.
- [x] Task: Conductor - User Manual Verification 'Phase 3: End-to-End Verification & Code Quality Gates' (Protocol in workflow.md)
