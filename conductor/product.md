# Initial Concept

Tool/script to extract tables from PDF files (like technical lists LE/LI) into XLSX Excel spreadsheets.

# Product Vision & Goals

A high-accuracy, privacy-focused Python CLI utility designed to convert complex tables from engineering and technical PDF documents (such as technical lists LE/LI: `R11.01-2151-LE-0001_2.pdf` and `R11.01-2151-LI-0001_3-1.pdf`) into clean, structured Excel (`.xlsx`) files.

## Target Audience & Use Case
- **Target Audience:** Engineers, technical project managers, data analysts, and administrative teams working with technical documentation and tabular data in PDF format.
- **Primary Use Case:** Extracting technical lists (e.g., Lista de Equipamentos / Lista de Instrumentos LE/LI) and standard multi-page PDF tables into perfectly structured XLSX files without manual copy-pasting or cloud API dependencies.

## Key Features & Architecture
- **Hybrid Extraction Engine:**
  - **Tier 1 (Fast Rule-Based Parsing):** Uses deterministic libraries (such as `pdfplumber` or `camelot`) to quickly extract structured tables with explicit gridlines or consistent text positioning.
  - **Tier 2 (Local AI Fallback):** Integrates an offline, locally hosted AI model (e.g., via Ollama / local vision model) to recognize complex, borderless, or non-standard tables when rule-based parsing confidence is low.
- **Offline & Private:** 100% local execution running on the host workstation. No external cloud service calls or sensitive data leakage.
- **CLI Workflows:** Flexible command-line interface supporting individual file conversion (`--file path/to/doc.pdf`), batch directory processing (`--dir path/to/folder/`), and extraction profile presets (`--profile generic` default for universal PDF tables or `--profile le_li` for industrial engineering sheets).
- **Rich XLSX Output:**
  - Preserves tabular structure, aligned headers, and typed values (numbers, dates, currency, text).
  - Multi-sheet Excel workbook export featuring individual sheets per table/page alongside a consolidated summary sheet.

## Non-Functional Requirements
- **Execution Overhead:** Tolerates longer processing time for local AI inferences provided extraction quality and table structure fidelity are preserved.
- **Portability:** Self-contained Python script/CLI executable on local Windows host.
