# Implementation Plan: Suporte a Extração Genérica de Tabelas em PDF (`generic_pdf_extraction`)

## Phase 1: Models & Profile Parameter Integration
- [x] Task: Expand CLI and Data Models for Profile Selection
    - [x] Add '--profile' parameter to CLI in 'cli.py' (options: 'generic', 'le_li', default: 'generic')
    - [x] Update extractor interfaces in 'models.py' and 'rule_based.py' to accept profile settings
    - [x] Write unit tests verifying CLI argument parsing for '--profile'
- [x] Task: Conductor - User Manual Verification 'Phase 1: Models & Profile Parameter Integration' (Protocol in workflow.md)

## Phase 2: Refactoring Cleaner for Generic & Profile-Based Cleaning
- [x] Task: Refactor cleaner.py into Modular Profile Cleaners
    - [x] Implement 'clean_generic_table_rows' for neutral sanitization and basic page number footer filtering
    - [x] Retain existing LE/LI cleaning logic under 'clean_le_li_table_rows' for 'le_li' profile
    - [x] Update 'RuleBasedExtractor' to dispatch to appropriate cleaner based on active profile
    - [x] Write unit tests for generic table cleaning without hardcoded LE/LI mutations
- [x] Task: Conductor - User Manual Verification 'Phase 2: Refactoring Cleaner for Generic & Profile-Based Cleaning' (Protocol in workflow.md)

## Phase 3: Integration Testing & Verification
- [x] Task: Integration Verification across Generic and LE/LI PDFs
    - [x] Test generic PDF extraction on sample PDFs to ensure no column corruption
    - [x] Test LE/LI PDF extraction with '--profile le_li' to ensure 100% backward compatibility
    - [x] Run full test suite ('pytest', 'ruff check .', 'mypy .')
- [x] Task: Conductor - User Manual Verification 'Phase 3: Integration Testing & Verification' (Protocol in workflow.md)

