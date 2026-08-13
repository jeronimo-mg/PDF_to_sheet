"""Cleaner module for multi-row header merging, cell text sanitization, and footer filtering."""

from typing import Any


def clean_cell_text(text: Any | None) -> str:
    """Clean linebreaks and whitespace from a cell string."""
    if text is None:
        return ""
    val = str(text).replace("\n", " ").strip()
    # Replace multiple internal spaces with single space
    while "  " in val:
        val = val.replace("  ", " ")
    return val


def is_footer_or_metadata_row(row: list[str | None]) -> bool:
    """Check if a table row represents a document footer or metadata block."""
    text_line = " ".join([clean_cell_text(c) for c in row if c])
    footer_keywords = [
        "Título :",
        "Sistema :",
        "Notas:",
        "Instalação :",
        "Nº. Fluxograma :",
        "Nº. Cliente :",
        "SITUAÇÃO DA REVISÃO",
        "DOCUMENTOS DE REFERÊNCIA",
        "ESTE DOCUMENTO É CONSTITUÍDO",
    ]
    for kw in footer_keywords:
        if kw.lower() in text_line.lower():
            return True
    return False


def merge_multiline_headers(rows: list[list[str | None]]) -> tuple[list[str], int]:
    """Detect if table has a 2-row split header and merge it vertically into a single list of column names."""
    if not rows:
        return [], 0

    if len(rows) < 2:
        clean_single = [clean_cell_text(c) for c in rows[0]]
        return clean_single, 1

    r0 = [clean_cell_text(c) for c in rows[0]]
    r1 = [clean_cell_text(c) for c in rows[1]]

    # Check if r1 looks like a sub-header row (e.g. contains 'Equipamento', 'Número (TAG)', etc. while r0 has empty/None in those positions)
    sub_header_indicators = ["equipamento", "número", "tag", "dimensões", "peso", "operacionais", "status", "book"]
    has_sub_headers = any(any(ind in c.lower() for ind in sub_header_indicators) for c in r1 if c)

    if has_sub_headers:
        merged_headers: list[str] = []
        max_cols = max(len(r0), len(r1))
        for i in range(max_cols):
            c0 = r0[i] if i < len(r0) else ""
            c1 = r1[i] if i < len(r1) else ""

            parts = []
            if c0:
                parts.append(c0)
            if c1:
                parts.append(c1)

            merged_headers.append(" / ".join(parts) if parts else "")

        return merged_headers, 2

    # Single-row header fallback
    return r0, 1


def clean_raw_table_rows(raw_rows: list[list[str | None]]) -> tuple[list[str], list[list[str]]]:
    """Clean raw table rows: merge headers, strip linebreaks, and filter out footer rows."""
    if not raw_rows:
        return [], []

    headers, data_start_idx = merge_multiline_headers(raw_rows)
    data_rows: list[list[str]] = []

    for r in raw_rows[data_start_idx:]:
        if is_footer_or_metadata_row(r):
            continue

        cleaned_row = [clean_cell_text(c) for c in r]
        # Drop trailing None/empty columns if they extend past headers count
        if len(cleaned_row) > len(headers):
            cleaned_row = cleaned_row[: len(headers)]
        # Pad row if shorter than headers
        while len(cleaned_row) < len(headers):
            cleaned_row.append("")

        if any(cell_text != "" for cell_text in cleaned_row):
            data_rows.append(cleaned_row)

    return headers, data_rows


def is_technical_data_table(table: Any) -> bool:
    """Classify if a TableData instance represents a primary technical equipment/instrument table vs metadata/revision block."""
    headers = getattr(table, "headers", [])
    if not headers:
        return False

    header_text = " ".join(str(h) for h in headers).lower()

    # Exclude cover page revision matrices
    if "situação da revisão" in header_text or "revisão de cada folha" in header_text:
        return False
    if "documentos de referência" in header_text and len(headers) < 4:
        return False

    # Positive signals for technical LE/LI data tables
    technical_keywords = ["tag", "equipamento", "instrumento", "serviço", "tipo", "pressão", "desenho", "número", "rev."]
    signal_count = sum(1 for kw in technical_keywords if kw in header_text)

    return signal_count >= 1
