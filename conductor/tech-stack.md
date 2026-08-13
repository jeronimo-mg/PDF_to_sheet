# Technology Stack

## Core Language & Runtime
- **Python 3.10+**: Primary programming language providing robust data processing libraries, native typing, and extensive ecosystem for PDF manipulation and Excel generation.

## PDF Parsing & Extraction Engine
- **pdfplumber**: Primary deterministic PDF text and table extraction engine. Excellent at extracting precise word positions, cell bounding boxes, and table lines.
- **Camelot (camelot-py / OpenCV)**: Secondary table parsing library specialized in lattice and stream table extraction from complex document layouts.
- **PyPDF / pypdfium2**: Fast low-level PDF page rendering and text extraction utility.

## Local AI & Vision Processing
- **Ollama / Local Vision Models**: Offline LLM/Vision runtime (e.g. `llama3.2-vision` or `llava`) running locally via Ollama HTTP API (`http://localhost:11434`) for fallback table structure recognition on unruled or complex PDF pages.
- **pdf2image / Pillow (PIL)**: High-resolution PDF page image rendering for local vision model consumption when visual layout analysis is required.

## Excel Generation & Formatting
- **pandas**: Core data structure manipulation (DataFrame) and tabular aggregation.
- **openpyxl**: Low-level Excel workbook writer used by pandas to create `.xlsx` files with rich formatting (custom fonts, column width auto-adjustment, cell fills for confidence highlights, multiple sheets).

## CLI & Terminal User Experience
- **Click / Typer**: Feature-rich CLI framework for command-line argument parsing, subcommands (`convert`, `batch`), flag validation, and help messages.
- **Rich**: Terminal formatting library providing modern progress bars, status spinners, colored logs, and interactive summary tables.

## Testing & Quality Assurance
- **pytest**: Framework for unit and integration testing.
- **pytest-cov**: Code coverage reporter.
- **mypy & ruff**: Static type checking and high-performance linting/formatting.
