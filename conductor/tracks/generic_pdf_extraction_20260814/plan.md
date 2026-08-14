# Implementation Plan: Suporte a Extração Genérica de Tabelas em PDF (`generic_pdf_extraction`)

## Phase 1: Models & Profile Parameter Integration
- [ ] Task: Expand CLI and Data Models for Profile Selection
    - [ ] Add '--profile' parameter to CLI in 'cli.py' (options: 'generic', 'le_li', default: 'generic')
    - [ ] Update extractor interfaces in 'models.py' and 'rule_based.py' to accept profile settings
    - [ ] Write unit tests verifying CLI argument parsing for '--profile'
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Models & Profile Parameter Integration' (Protocol in workflow.md)

## Phase 2: Refactoring Cleaner for Generic & Profile-Based Cleaning
- [ ] Task: Refactor cleaner.py into Modular Profile Cleaners
    - [ ] Implement 'clean_generic_table_rows' for neutral sanitization and basic page number footer filtering
    - [ ] Retain existing LE/LI cleaning logic under 'clean_le_li_table_rows' for 'le_li' profile
    - [ ] Update 'RuleBasedExtractor' to dispatch to appropriate cleaner based on active profile
    - [ ] Write unit tests for generic table cleaning without hardcoded LE/LI mutations
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Refactoring Cleaner for Generic & Profile-Based Cleaning' (Protocol in workflow.md)

## Phase 3: Integration Testing & Verification
- [ ] Task: Integration Verification across Generic and LE/LI PDFs
    - [ ] Test generic PDF extraction on sample PDFs to ensure no column corruption
    - [ ] Test LE/LI PDF extraction with '--profile le_li' to ensure 100% backward compatibility
    - [ ] Run full test suite ('pytest', 'ruff check .', 'mypy .')
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Integration Testing & Verification' (Protocol in workflow.md)
