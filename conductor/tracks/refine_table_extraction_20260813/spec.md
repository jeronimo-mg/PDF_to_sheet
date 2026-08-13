# Track Specification: Refinar Extração de Tabelas LE/LI com Fusão de Cabeçalhos Multi-Linha e Filtro de Capa

## 1. Overview
- **Track ID:** `refine_table_extraction_20260813`
- **Type:** Enhancement / Refactoring
- **Goal:** Upgrade the PDF table extraction engine (`RuleBasedExtractor` and `HybridTableExtractor`) to filter cover page revision matrices, merge multi-row headers into clean single-row column titles, and format equipment sub-rows into clean Excel spreadsheets without column shifting.

## 2. Functional Requirements
1. **Cover Page & Metadata Table Filtering:**
   - Detect cover page revision blocks (e.g. `SITUAÇÃO DA REVISÃO DAS FOLHAS`, `DOCUMENTOS DE REFERÊNCIA`) and exclude them from the `Master_Consolidated` equipment dataset.
   - Restrict `Master_Consolidated` strictly to primary technical data tables (containing `TAG`, `Equipamento`, `Instrumento`, `Serviço`).
2. **Multi-Row Header Detection & Merging:**
   - Detect 2-row table headers (e.g. Row 0: `Identificação`, Row 1: `Equipamento` / `Número (TAG)`).
   - Merge split header cells vertically using `' / '` separator (resulting in `Identificação / Equipamento`, `Número (TAG)`).
   - Strip all internal linebreaks (`\n`) from header text.
3. **Sub-Row & Cell Content Formatting:**
   - Replace internal `\n` in cell data with single spaces for clean Excel presentation.
   - Group sub-row details (e.g. `(CASCO)` or `(TUBOS)`) into continuous, correctly aligned rows.
   - Remove document footer blocks (`Título: ÍNDICE DE EQUIPAMENTOS...`, `Notas: ...`) from main data rows.

## 3. Non-Functional Requirements & Quality Criteria
- **Empirical Validation:** 100% clean column alignment and header formatting on `R11.01-2151-LE-0001_2.pdf` and `R11.01-2151-LI-0001_3-1.pdf`.
- **Unit Testing & Coverage:** Unit tests verifying multi-row header merging, cover page filtering, and cell cleaning in `tests/`.
- **Static Analysis:** Zero errors on `ruff check .` and `mypy src`.
