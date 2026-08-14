"""Unit tests for Excel formatting (max column width capping and text wrapping)."""

import openpyxl

from typing import Any

from pdf_to_sheet.models import ExtractionResult, TableData
from pdf_to_sheet.writers.excel import ExcelWriter


def test_excel_writer_caps_max_column_width_and_enables_wrap_text(tmp_path: Any) -> None:
    headers = ["Rev.", "Descricao Longa", "Tag"]
    long_text = "X" * 300  # 300 characters long string
    row = ["1", long_text, "2151-TC01"]

    table = TableData(headers=headers, rows=[row], page_number=1)
    res = ExtractionResult(source_file="test.pdf", tables=[table], extractor_used="Test", success=True)

    out_file = str(tmp_path / "formatted.xlsx")
    writer = ExcelWriter()
    writer.write(res, out_file)

    wb = openpyxl.load_workbook(out_file)
    ws = wb["Master_Consolidated"]

    # Verify column B width is capped at 45
    assert ws.column_dimensions["B"].width <= 45.0
    assert ws.column_dimensions["A"].width >= 10.0

    # Verify cell alignment wrap_text is True and vertical is top
    data_cell = ws["B2"]
    assert data_cell.alignment.wrap_text is True
    assert data_cell.alignment.vertical == "top"
