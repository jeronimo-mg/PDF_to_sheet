# Product Guidelines & Standards

## User Experience & CLI Feedback
- **Informative Terminal Output:** Use modern, clean terminal progress feedback (e.g., `rich` or `tqdm`) displaying clear extraction stages:
  1. PDF Parsing & Layout Analysis
  2. Table Extraction & AI Fallback (if triggered)
  3. XLSX Formatting & Multi-sheet Generation
- **Clarity over Silence:** Provide actionable status messages and visual indicators for file progress without cluttering stdout with raw tracebacks.

## Error Handling & Data Integrity
- **Zero Loss Principle:** Never silently drop ambiguous rows or columns. Highlight low-confidence or unparsed cells directly in Excel output (e.g., light yellow cell fill or cell comment) and generate a `.log` report.
- **Strict Schema Validation:** Option to validate extracted headers against target document types (e.g., LE/LI technical equipment lists) and alert the user if critical columns are missing.
- **Graceful Fallback Pipeline:**
  1. Deterministic grid-based parsing (`pdfplumber` / `camelot`).
  2. Spatial raw-text matching fallback if grid lines are absent.
  3. Local AI model vision inference fallback if visual structure is complex or unruled.

## Local AI Model Execution Policy
- **Auto-Detection & Resilience:** Automatically check host system for local AI services (e.g., Ollama HTTP endpoint or local model runner). If unavailable or offline, gracefully degrade to rule-based and spatial text parsing with a user alert.
- **Privacy First:** 100% offline data processing. Zero external network API requests.

## Code Quality & Architecture Standards
- **Modular Strategy Pattern:** Decouple PDF extraction algorithms (`PdfPlumberExtractor`, `CamelotExtractor`, `LocalAIExtractor`) behind a clean, unified `TableExtractor` interface.
- **Strict Typing:** Require explicit Python type hints, dataclasses for internal representations (e.g., `TableData`, `Cell`, `ExtractionResult`), and docstrings for all modules and public methods.
- **Test Coverage:** Build unit tests with synthetic and sample PDF table fixtures to verify parsing accuracy, edge cases, and XLSX layout rendering.
