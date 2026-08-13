"""Unit tests for row sanitization, cell 0 corruption repair, and TAG propagation."""

from pdf_to_sheet.cleaner import sanitize_table_rows


def test_sanitize_table_rows_fixes_corrupted_rev_cell() -> None:
    headers = ["Rev.", "Identificação / Equipamento", "Número (TAG)", "Classe Segur."]
    corrupted_row = [
        "Q = 10 m³/h; Tamanho Aço inox. 1 FILTRO 2151-FT03 CS-NN Reter resina CARTUCHO 5,0 55,0",
        "FILTRO",
        "2151-FT03",
        "CS-NN",
    ]
    normal_row = ["1", "DESIONIZADOR", "2151-DZ01", "CS-1"]

    _, clean_r = sanitize_table_rows(headers, [normal_row, corrupted_row])

    assert clean_r[1][0] == "1"
    assert clean_r[1][2] == "2151-FT03"


def test_sanitize_table_rows_propagates_parent_tag_to_subrows() -> None:
    headers = ["Rev.", "Identificação / Equipamento", "Número (TAG)", "Classe Segur."]
    parent_row = ["1", "TROC DE CALOR REGEN. (TUBOS)", "2151-TC01", "CS-1"]
    sub_row = ["", "(CASCO)", "", ""]

    _, clean_r = sanitize_table_rows(headers, [parent_row, sub_row])

    assert clean_r[1][0] == "1"
    assert clean_r[1][2] == "2151-TC01 (CASCO)"


def test_sanitize_table_rows_drops_empty_trailing_headers() -> None:
    headers = ["Rev.", "Identificação / Equipamento", "Número (TAG)", ""]
    row = ["1", "DESIONIZADOR", "2151-DZ01", "CS-1"]

    clean_h, clean_r = sanitize_table_rows(headers, [row])

    assert len(clean_h) == 3
    assert clean_h == ["Rev.", "Identificação / Equipamento", "Número (TAG)"]
    assert len(clean_r[0]) == 3
