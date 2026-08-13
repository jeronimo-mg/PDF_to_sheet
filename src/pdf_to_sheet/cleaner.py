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

    return sanitize_table_rows(headers, data_rows)


def sanitize_table_rows(headers: list[str], rows: list[list[str]]) -> tuple[list[str], list[list[str]]]:
    """Sanitize table headers and rows: drop trailing empty headers, fix cell 0 artifacts, propagate TAGs to subrows."""
    clean_headers = list(headers)
    while clean_headers and not clean_headers[-1].strip():
        clean_headers.pop()

    if not clean_headers or not rows:
        return clean_headers, []

    sanitized_rows: list[list[str]] = []
    last_rev = "1"
    last_tag = ""

    for row in rows:
        r = list(row[: len(clean_headers)])
        while len(r) < len(clean_headers):
            r.append("")

        # 1. Fix cell 0 (Rev.) corruptions/artifacts
        rev_val = r[0].strip() if len(r) > 0 else ""
        if len(rev_val) > 10 or "FILTRO" in rev_val or "TROC" in rev_val:
            r[0] = last_rev
        elif rev_val:
            last_rev = rev_val
        else:
            r[0] = last_rev

        # 2. TAG propagation for sub-rows (e.g. (CASCO))
        tag_col_idx = 2  # Default TAG index for LE/LI tables
        if len(r) > tag_col_idx:
            current_tag = r[tag_col_idx].strip()
            if current_tag:
                last_tag = current_tag
            elif len(r) > 1 and r[1] and "(CASCO)" in r[1]:
                r[tag_col_idx] = f"{last_tag} (CASCO)" if last_tag else "(CASCO)"

        sanitized_rows.append(r)

    return clean_headers, sanitized_rows


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
