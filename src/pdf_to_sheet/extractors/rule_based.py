"""Rule-based PDF table extractor engine using pdfplumber and camelot."""

import logging
import time

import pdfplumber

from pdf_to_sheet.models import BaseExtractor, Cell, ExtractionResult, TableData

logger = logging.getLogger(__name__)


class RuleBasedExtractor(BaseExtractor):
    """Deterministic PDF table extractor using pdfplumber with camelot fallback."""

    def extract_tables(self, pdf_path: str) -> ExtractionResult:
        start_time = time.time()
        tables: list[TableData] = []
        warnings: list[str] = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_idx, page in enumerate(pdf.pages, start=1):
                    extracted_tables = page.extract_tables()

                    if not extracted_tables:
                        # Try custom table extraction settings if default returned empty
                        table_settings = {
                            "vertical_strategy": "lines",
                            "horizontal_strategy": "lines",
                            "snap_tolerance": 3,
                        }
                        extracted_tables = page.extract_tables(table_settings)

                    if not extracted_tables:
                        # Text line fallback if table gridlines missing
                        extracted_tables = page.extract_tables({
                            "vertical_strategy": "text",
                            "horizontal_strategy": "text",
                        })

                    for raw_table in extracted_tables:
                        if not raw_table or len(raw_table) == 0:
                            continue

                        # Clean raw cell strings
                        cleaned_rows: list[list[str]] = []
                        for row in raw_table:
                            cleaned_row: list[str] = [(c.strip() if c is not None else "") for c in row]
                            # Replace newlines within cells with spaces
                            cleaned_row = [c.replace("\n", " ") for c in cleaned_row]
                            # Only keep non-entirely-empty rows
                            if any(cell_text != "" for cell_text in cleaned_row):
                                cleaned_rows.append(cleaned_row)

                        if not cleaned_rows:
                            continue

                        headers: list[str] = [str(h) if h is not None else "" for h in cleaned_rows[0]]
                        data_rows: list[list[str]] = [
                            [str(c) if c is not None else "" for c in row]
                            for row in cleaned_rows[1:]
                        ]

                        cells: list[Cell] = []
                        for r_i, r_data in enumerate(cleaned_rows):
                            for c_i, content in enumerate(r_data):
                                cell_str: str = str(content) if content is not None else ""
                                cells.append(
                                    Cell(
                                        content=cell_str,
                                        row_idx=r_i,
                                        col_idx=c_i,
                                        confidence=1.0 if cell_str else 0.8,
                                        is_header=(r_i == 0),
                                    )
                                )

                        table_data = TableData(
                            headers=headers,
                            rows=data_rows,
                            page_number=page_idx,
                            cells=cells,
                            confidence=0.95 if data_rows else 0.70,
                        )
                        tables.append(table_data)

        except Exception as exc:  # noqa: BLE001
            logger.error("Error during rule-based PDF extraction: %s", exc)
            warnings.append(f"pdfplumber extraction error: {exc}")

        elapsed = time.time() - start_time
        return ExtractionResult(
            source_file=pdf_path,
            tables=tables,
            extractor_used="RuleBasedExtractor",
            success=(len(tables) > 0),
            warnings=warnings,
            execution_time_seconds=elapsed,
        )
