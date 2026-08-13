"""Tests for multi-page table assembly and header merging."""

from pdf_to_sheet.merger import merge_tables
from pdf_to_sheet.models import TableData


def test_merge_tables_with_matching_headers() -> None:
    headers = ["ITEM", "TAG", "DESCRIPTION", "QTY"]
    table1 = TableData(
        headers=headers,
        rows=[["1", "P-101", "Bomba 1", "1"]],
        page_number=1,
    )
    table2 = TableData(
        headers=headers,
        rows=[["2", "P-102", "Bomba 2", "1"]],
        page_number=2,
    )

    merged = merge_tables([table1, table2])
    assert len(merged) == 1
    assert merged[0].headers == headers
    assert len(merged[0].rows) == 2
    assert merged[0].rows[0][1] == "P-101"
    assert merged[0].rows[1][1] == "P-102"


def test_merge_tables_with_different_headers() -> None:
    t1 = TableData(headers=["A", "B"], rows=[["1", "2"]], page_number=1)
    t2 = TableData(headers=["X", "Y"], rows=[["9", "8"]], page_number=2)

    merged = merge_tables([t1, t2])
    assert len(merged) == 2
    assert merged[0].headers == ["A", "B"]
    assert merged[1].headers == ["X", "Y"]
