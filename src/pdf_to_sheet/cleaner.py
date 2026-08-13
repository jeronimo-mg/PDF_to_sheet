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


def preprocess_mixed_header_data_rows(raw_rows: list[list[str | None]]) -> list[list[str | None]]:
    """Detect and split rows where sub-header keywords (SISTEMA, INSTRUM., MEC, ELE) are mixed with data values."""
    new_rows: list[list[str | None]] = []

    for row in raw_rows:
        has_mixed = False
        header_part: list[str | None] = [None] * len(row)
        data_part: list[str | None] = [None] * len(row)

        for i, cell in enumerate(row):
            if not cell:
                continue
            text = str(cell).strip()

            if "SISTEMA" in text and text != "SISTEMA":
                header_part[i] = "SISTEMA"
                data_part[i] = text.replace("SISTEMA", "").strip()
                has_mixed = True
            elif "INSTRUM." in text and text != "INSTRUM.":
                header_part[i] = "INSTRUM."
                data_part[i] = text.replace("INSTRUM.", "").strip()
                has_mixed = True
            elif "MEC" in text and len(text) > 3 and text.startswith("MEC"):
                header_part[i] = "MEC"
                data_part[i] = text.replace("MEC", "").strip()
                has_mixed = True
            elif "ELE" in text and len(text) > 3 and text.startswith("ELE"):
                header_part[i] = "ELE"
                data_part[i] = text.replace("ELE", "").strip()
                has_mixed = True
            elif text in ["SISTEMA", "INSTRUM.", "MEC", "ELE"]:
                header_part[i] = text
            else:
                data_part[i] = text

        if has_mixed:
            if any(h for h in header_part if h):
                new_rows.append(header_part)
            if any(d for d in data_part if d):
                new_rows.append(data_part)
        else:
            new_rows.append(row)

    return new_rows


def merge_multiline_headers(rows: list[list[str | None]]) -> tuple[list[str], int]:
    """Detect if table has a 2-row split header and merge it vertically into a single list of column names."""
    if not rows:
        return [], 0

    if len(rows) < 2:
        clean_single = [clean_cell_text(c) for c in rows[0]]
        return clean_single, 1

    r0 = [clean_cell_text(c) for c in rows[0]]
    r1 = [clean_cell_text(c) for c in rows[1]]

    sub_header_indicators = ["equipamento", "número", "tag", "dimensões", "peso", "operacionais", "status", "book", "sistema", "instrum", "linha", "coord"]
    is_r1_subheader = any(any(ind in c.lower() for ind in sub_header_indicators) for c in r1 if c)
    is_r1_data = r1[0].strip() in ["0", "1", "2", "3", "4", "5"] or any("DZ-" in c or "P-" in c for c in r1 if c)

    if is_r1_subheader and not is_r1_data:
        merged_headers: list[str] = []
        max_cols = max(len(r0), len(r1))
        for i in range(max_cols):
            c0 = r0[i] if i < len(r0) else ""
            c1 = r1[i] if i < len(r1) else ""

            parts = []
            if c0:
                parts.append(c0)
            if c1 and c1 not in parts:
                parts.append(c1)

            merged_headers.append(" / ".join(parts) if parts else "")

        return merged_headers, 2

    return r0, 1


def clean_raw_table_rows(raw_rows: list[list[str | None]]) -> tuple[list[str], list[list[str]]]:
    """Clean raw table rows: preprocess mixed headers, merge multi-line headers, strip linebreaks, and filter footers."""
    if not raw_rows:
        return [], []

    preprocessed_rows = preprocess_mixed_header_data_rows(raw_rows)
    headers, data_start_idx = merge_multiline_headers(preprocessed_rows)
    data_rows: list[list[str]] = []

    for r in preprocessed_rows[data_start_idx:]:
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


def merge_adjacent_item_rows(rows: list[list[str]], num_cols: int) -> list[list[str]]:
    """Merge sparse adjacent sub-rows for the same item/equipment into a single consolidated row."""
    if not rows:
        return []

    merged: list[list[str]] = []
    current_row: list[str] | None = None

    for row in rows:
        rev = row[0].strip() if len(row) > 0 else ""
        if current_row and (not rev or rev == current_row[0]):
            # Check if combining fills empty slots in current_row
            can_merge = False
            for col_idx in range(min(len(row), num_cols)):
                if not current_row[col_idx] and row[col_idx]:
                    can_merge = True
                    break
            if can_merge:
                for col_idx in range(min(len(row), num_cols)):
                    if not current_row[col_idx] and row[col_idx]:
                        current_row[col_idx] = row[col_idx]
                    elif current_row[col_idx] and row[col_idx] and current_row[col_idx] != row[col_idx] and col_idx >= num_cols - 2:
                        current_row[col_idx] += " " + row[col_idx]
                continue

        current_row = list(row)
        merged.append(current_row)

    return merged


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

    # 3. Merge adjacent sparse item sub-rows into single consolidated rows
    consolidated_rows = merge_adjacent_item_rows(sanitized_rows, len(clean_headers))

    return clean_headers, consolidated_rows


def is_technical_data_table(table: Any) -> bool:
    """Classify if a TableData instance represents a primary technical equipment/instrument table vs metadata/revision block."""
    headers = getattr(table, "headers", [])
    if not headers:
        return False

    header_text = " ".join(str(h) for h in headers).lower()

    # Exclude cover page revision matrices & cover metadata
    if "situação da revisão" in header_text or "revisão de cada folha" in header_text:
        return False
    if "documentos de referência" in header_text and len(headers) < 4:
        return False

    # Positive signals for technical LE/LI data tables
    technical_keywords = ["tag", "equipamento", "instrumento", "serviço", "tipo", "pressão", "desenho", "número", "rev.", "qty", "descricao"]
    signal_count = sum(1 for kw in technical_keywords if kw in header_text)

    return signal_count >= 1
