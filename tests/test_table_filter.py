"""Tests for technical table classification and metadata filtering."""

from pdf_to_sheet.cleaner import is_technical_data_table
from pdf_to_sheet.models import TableData


def test_is_technical_data_table_positive() -> None:
    headers = ["Rev.", "Identificação / Equipamento", "Número (TAG)", "Classe Segur."]
    t = TableData(headers=headers, rows=[["1", "DESIONIZADOR", "DZ01", "CS-1"]], page_number=2)
    assert is_technical_data_table(t) is True


def test_is_technical_data_table_negative_cover() -> None:
    headers = ["SITUAÇÃO DA REVISÃO DAS FOLHAS\nREV. REVISÃO DE CADA FOLHA\n1 2 42 83 124"]
    t = TableData(headers=headers, rows=[["1", "2", "3"]], page_number=1)
    assert is_technical_data_table(t) is False
