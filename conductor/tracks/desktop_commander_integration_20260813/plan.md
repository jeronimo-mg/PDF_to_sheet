# Implementation Plan: Integração do Desktop Commander Local com Motor pdf-to-sheet e Ollama

Build a local MCP server wrapper (`src/pdf_to_sheet/mcp_server.py`) and Desktop Commander configuration templates to expose offline PDF-to-XLSX conversion capabilities to local Desktop Commander and Ollama.

## Proposed Phased Development

### Phase 1: Local MCP Server Wrapper & Tool Handlers
- [ ] Task: MCP Server Module & Tool Registration
    - [ ] Write unit tests for MCP tool handlers in `tests/test_mcp_server.py`.
    - [ ] Implement `convert_pdf`, `batch_convert_dir`, and `inspect_pdf_tables` MCP handlers in `src/pdf_to_sheet/mcp_server.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Local MCP Server Wrapper & Tool Handlers' (Protocol in workflow.md)

### Phase 2: Desktop Commander & Ollama Configuration Templates
- [ ] Task: Configuration Templates & CLI Integration
    - [ ] Write unit tests for configuration file loading and Ollama endpoint verification in `tests/test_mcp_config.py`.
    - [ ] Create Desktop Commander integration configs (`mcp_config.json` and `claude_desktop_config.json`) and CLI entrypoint `pdf-to-sheet-mcp`.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Desktop Commander & Ollama Configuration Templates' (Protocol in workflow.md)

### Phase 3: End-to-End Empirical Verification & Code Quality Gates
- [ ] Task: End-to-End Desktop Automation Verification
    - [ ] Perform empirical MCP tool execution tests on `R11.01-2151-LE-0001_2.pdf` and `R11.01-2151-LI-0001_3-1.pdf`.
    - [ ] Run static analysis (`ruff check .`, `mypy src`) and full test suite (`pytest`) ensuring clean pass.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: End-to-End Empirical Verification & Code Quality Gates' (Protocol in workflow.md)
