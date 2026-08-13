"""Unit tests for cleaner module (header merging and text sanitization)."""

from pdf_to_sheet.cleaner import clean_cell_text, clean_raw_table_rows, merge_multiline_headers


def test_clean_cell_text() -> None:
    assert clean_cell_text("Identificação\nEquipamento") == "Identificação Equipamento"
    assert clean_cell_text("  P=248,5 kW  \n(100% pot) ") == "P=248,5 kW (100% pot)"
    assert clean_cell_text(None) == ""


def test_merge_multiline_headers_2_rows() -> None:
    row0 = ["Rev.", "Identificação", None, "Classe\nSegur.", "Serviço"]
    row1 = [None, "Equipamento", "Número\n(TAG)", None, None]

    headers, data_start_idx = merge_multiline_headers([row0, row1, ["1", "BOMBA", "TAG-1", "CS-1", "Agua"]])

    assert data_start_idx == 2
    assert headers[0] == "Rev."
    assert headers[1] == "Identificação / Equipamento"
    assert headers[2] == "Número (TAG)"
    assert headers[3] == "Classe Segur."
    assert headers[4] == "Serviço"


def test_clean_raw_table_rows() -> None:
    raw_rows = [
        ["Rev.", "Identificação", None],
        [None, "Equipamento", "Número\n(TAG)"],
        ["1", "DESIONIZADOR\nCILINDRICO", "DZ-01"],
        ["Notas: 1- Cancelada", None, None],
        ["Título : ÍNDICE DE EQUIPAMENTOS", None, None],
    ]

    cleaned_headers, data_rows = clean_raw_table_rows(raw_rows)
    assert cleaned_headers == ["Rev.", "Identificação / Equipamento", "Número (TAG)"]
    assert len(data_rows) == 1
    assert data_rows[0] == ["1", "DESIONIZADOR CILINDRICO", "DZ-01"]
