"""Unit tests for ExcelWriter module."""

import os
from typing import Any

import openpyxl

from pdf_to_sheet.models import ExtractionResult, TableData
from pdf_to_sheet.writers.excel import ExcelWriter


def test_excel_writer_creates_xlsx(tmp_path: Any) -> None:
    output_path = str(tmp_path / "output.xlsx")

    t1 = TableData(headers=["TAG", "QTY"], rows=[["P-101", "2"], ["P-102", "4"]], page_number=1)
    t2 = TableData(headers=["TAG", "QTY"], rows=[["P-201", "1"]], page_number=2)

    result = ExtractionResult(
        source_file="test.pdf",
        tables=[t1, t2],
        extractor_used="TestExtractor",
        success=True,
    )

    writer = ExcelWriter()
    written_file = writer.write(result, output_path)

    assert os.path.exists(written_file)

    wb = openpyxl.load_workbook(written_file)
    sheet_names = wb.sheetnames
    assert "Master_Consolidated" in sheet_names
    assert "Table_1_Page_1" in sheet_names
    assert "Table_2_Page_2" in sheet_names
