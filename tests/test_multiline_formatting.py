"""Unit test for preserving \n linebreaks in 2-line fields (SERVIÇO, FLUXOGRAMA, FOLHA DE DADOS)."""

from pdf_to_sheet.cleaner import merge_adjacent_item_rows


def test_merge_adjacent_item_rows_preserves_linebreaks() -> None:
    rows = [
        ["1", "2151", "TE- 1501", "", "CS-1", "N1E", "", "", "TEMP. NA ENTRADA DO TROCADOR DE CALOR", "R11.01-2151-XE-0001"],
        ["1", "", "", "", "", "", "SISM-1", "", "1ADR-2151-001-1F70 /", "G-5"],
    ]

    merged = merge_adjacent_item_rows(rows, num_cols=10)
    assert len(merged) == 1
    item = merged[0]
    assert "TEMP. NA ENTRADA DO TROCADOR DE CALOR\n1ADR-2151-001-1F70 /" in item[8]
    assert "R11.01-2151-XE-0001\nG-5" in item[9]
