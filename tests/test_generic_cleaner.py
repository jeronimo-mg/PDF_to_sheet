"""Tests for generic profile table cleaning."""

from pdf_to_sheet.cleaner import clean_raw_table_rows, is_generic_footer_row


def test_is_generic_footer_row() -> None:
    assert is_generic_footer_row(["Página 1 de 5"]) is True
    assert is_generic_footer_row(["Page 3 of 10"]) is True
    assert is_generic_footer_row(["10 de 12"]) is True
    assert is_generic_footer_row(["Nome do Produto", "Preço", "Quantidade"]) is False


def test_clean_raw_table_rows_generic_preserves_columns() -> None:
    raw: list[list[str | None]] = [
        ["Código Produto", "Descrição Completa do Item", "Especificação", "Valor R$"],
        ["PROD-001", "Filtro de Ar Industrial Completo 2026", "MEC-SISTEMA 123", "1500.00"],
        ["PROD-002", "Bomba Trocador com mais de 10 caracteres", "(CASCO Especial)", "3200.50"],
        ["Página 1 de 2", None, None, None]
    ]

    headers, rows = clean_raw_table_rows(raw, profile="generic")

    assert headers == ["Código Produto", "Descrição Completa do Item", "Especificação", "Valor R$"]
    assert len(rows) == 2

    # Verify Column 0 is NOT mutated by last_rev logic
    assert rows[0][0] == "PROD-001"
    assert rows[1][0] == "PROD-002"

    # Verify Column 2 is NOT mutated by (CASCO) logic
    assert rows[0][2] == "MEC-SISTEMA 123"
    assert rows[1][2] == "(CASCO Especial)"
