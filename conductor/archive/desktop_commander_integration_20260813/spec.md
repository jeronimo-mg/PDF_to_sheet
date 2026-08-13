# Track Specification: Integração do Desktop Commander Local com Motor pdf-to-sheet e Ollama

## 1. Overview
- **Track ID:** `desktop_commander_integration_20260813`
- **Type:** Feature / Integration
- **Goal:** Create a local MCP (Model Context Protocol) server interface (`src/pdf_to_sheet/mcp_server.py`) and Desktop Commander configuration templates to allow local AI assistants and Desktop Commander to trigger offline PDF-to-XLSX conversions, inspect tables, and automate desktop file workflows using local Ollama models.

## 2. Functional Requirements
1. **Local MCP Server Module (`src/pdf_to_sheet/mcp_server.py`):**
   - Implement an MCP server wrapper exposing tools:
     - `convert_pdf(pdf_path: str, output_path: str)`: Convert a single PDF to a formatted Excel workbook.
     - `batch_convert_dir(input_dir: str, output_dir: str)`: Convert all PDFs in a directory.
     - `inspect_pdf_tables(pdf_path: str)`: Return table structures and page counts for local AI inspection.
2. **Desktop Commander & Ollama Configuration:**
   - Create `mcp_config.json` and `claude_desktop_config.json` configuration templates mapping `pdf-to-sheet` tools and local Ollama (`http://localhost:11434`).
   - Integrate local vision models (`llama3.2-vision`, `qwen2-vl`, `llava`) for visual table verification.
3. **Automated Desktop File Management:**
   - Auto-organize output files into structured destination folders (e.g. `output/LE/`, `output/LI/`).
   - Log execution metrics and row count validations to `logs/conversion.log`.

## 3. Non-Functional Requirements & Quality Criteria
- **100% Offline & Private:** Zero external network calls. All processing runs on `localhost`.
- **Integration Testing:** End-to-end test verifying MCP tool execution on `R11.01-2151-LE-0001_2.pdf` and `R11.01-2151-LI-0001_3-1.pdf`.
- **Static Analysis & Testing:** 100% pass on `pytest`, `ruff check .`, and `mypy src`.
