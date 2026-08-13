"""Unit test for preserving drawing coordinates (e.g. G-5, G-6) in multiline FLUXOGRAMA/COORD column."""

from pdf_to_sheet.cleaner import merge_adjacent_item_rows


def test_merge_adjacent_item_rows_preserves_coordinates() -> None:
    rows = [
        ["1", "2151", "TE- 1501", "", "CS-1", "N1E", "", "", "TEMP. NA ENTRADA DO TROCADOR DE CALOR", "R11.01-2151-XE-0001"],
        ["1", "2151", "", "", "", "", "SISM-1", "", "1ADR-2151-001-1F70 /", "G-5"],
    ]

    merged = merge_adjacent_item_rows(rows, num_cols=10)
    assert len(merged) == 1
    item = merged[0]
    assert "G-5" in item[9]
    assert "R11.01-2151-XE-0001\nG-5" in item[9]
