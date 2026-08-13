"""Tests for core data models and abstract extractor interface."""

from pdf_to_sheet.models import Cell, ExtractionResult, TableData


def test_cell_creation() -> None:
    cell = Cell(content="TAG-101", row_idx=0, col_idx=0, confidence=0.95)
    assert cell.content == "TAG-101"
    assert cell.row_idx == 0
    assert cell.col_idx == 0
    assert cell.confidence == 0.95


def test_table_data_creation() -> None:
    headers = ["TAG", "DESCRIPTION", "QTY"]
    rows = [
        ["TAG-01", "Bomba Centrifuga", "2"],
        ["TAG-02", "Válvula de Esfera", "5"],
    ]
    table = TableData(headers=headers, rows=rows, page_number=1)
    assert table.headers == headers
    assert len(table.rows) == 2
    assert table.page_number == 1
    assert table.row_count == 2
    assert table.col_count == 3


def test_extraction_result_creation() -> None:
    table = TableData(headers=["A", "B"], rows=[["1", "2"]], page_number=1)
    result = ExtractionResult(
        source_file="sample.pdf",
        tables=[table],
        extractor_used="RuleBased",
        success=True,
    )
    assert result.source_file == "sample.pdf"
    assert len(result.tables) == 1
    assert result.success is True
    assert result.extractor_used == "RuleBased"
