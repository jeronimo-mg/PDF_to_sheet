# Development Workflow

## 1. Branching & Commit Policy
- **Feature Branching:** Develop all tracks on dedicated feature branches named `feature/<track-id>` (e.g., `feature/pdf-table-parser`).
- **Commit Conventions:** Write concise, imperative commit messages referencing the active track ID (e.g., `feat(pdf-parser): implement rule-based table extractor`).
- **Main Branch Protection:** Merge feature branches into `main` only after all quality gates pass successfully.

## 2. Development & Quality Gates
Before marking any task or track as complete in Conductor, verify:
1. **Automated Unit Tests:** Execute `pytest` and ensure all test cases pass without errors.
2. **Empirical Validation:** Run the CLI parser directly against real sample PDF files (`R11.01-2151-LE-0001_2.pdf` and `R11.01-2151-LI-0001_3-1.pdf`) and inspect the output `.xlsx` file for column alignment, data types, and header accuracy.
3. **Static Analysis & Linting:** Run `ruff check .` and `mypy .` to verify zero linting or type errors.

## 3. Local AI & Integration Testing Protocol
- **Service Detection:** Automatically detect local AI runtime status (Ollama service at `http://localhost:11434`).
- **Conditional Testing:** If Ollama is active, run full AI vision fallback integration tests. If offline, gracefully skip live AI network calls while asserting rule-based fallback mechanics.

## 4. Documentation & Conductor Maintenance
- **Track Progress Updates:** Continuously update `plan.md` and top-level `index.md` as tasks transition between `[ ]` (Pending), `[~]` (In Progress), and `[x]` (Completed).
- **Execution Audit Logging:** Store conversion run logs and extraction stats in a structured `logs/` directory for debugging and auditability.
