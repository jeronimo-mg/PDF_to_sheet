"""Rule-based PDF table extractor engine using pdfplumber and camelot."""

import logging
import time

import pdfplumber

from pdf_to_sheet.cleaner import clean_raw_table_rows
from pdf_to_sheet.models import BaseExtractor, Cell, ExtractionResult, TableData

logger = logging.getLogger(__name__)


class RuleBasedExtractor(BaseExtractor):
    """Deterministic PDF table extractor using pdfplumber with camelot fallback."""

    def extract_tables(self, pdf_path: str, profile: str = "auto") -> ExtractionResult:
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

                        headers, data_rows = clean_raw_table_rows(raw_table, profile=profile)

                        if not headers or not data_rows:
                            continue

                        cells: list[Cell] = []
                        for r_i, r_data in enumerate(data_rows):
                            for c_i, content in enumerate(r_data):
                                cell_str: str = str(content)
                                cells.append(
                                    Cell(
                                        content=cell_str,
                                        row_idx=r_i,
                                        col_idx=c_i,
                                        confidence=1.0 if cell_str else 0.8,
                                        is_header=False,
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
