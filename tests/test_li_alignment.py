"""Unit test for LI sub-header text separation and column alignment."""

from pdf_to_sheet.cleaner import preprocess_mixed_header_data_rows


def test_split_mixed_header_data_rows() -> None:
    raw_rows = [
        ["PRÉDIO R11.01", "SISTEMA", "INSTRUM. TE- 1501", None, "MEC CS-1", "ELE N1E", None, None, None],
        ["R11.01", "2151", "TT- 1501", "C", "CS-NN", "N1E", None, None, "TEMP. NA ENTRADA DO TROCADOR DE CALOR"],
    ]

    processed = preprocess_mixed_header_data_rows(raw_rows)
    assert len(processed) >= 2
    # Verify SISTEMA and INSTRUM. are separated from data values
    header_row = processed[0]
    data_row = processed[1]
    assert header_row[1] == "SISTEMA"
    assert header_row[2] == "INSTRUM."
    assert "TE- 1501" in str(data_row[2]) or any("TE- 1501" in str(c) for c in data_row if c)
