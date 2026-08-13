"""Multi-page table assembly and header matching merger module."""


from pdf_to_sheet.models import TableData


def normalize_header(headers: list[str]) -> list[str]:
    """Normalize headers for string comparison."""
    return [h.strip().upper() for h in headers]


def merge_tables(tables: list[TableData]) -> list[TableData]:
    """Merge continuous tables across consecutive pages if headers match."""
    if not tables:
        return []

    merged: list[TableData] = []
    current: TableData = tables[0]

    for next_table in tables[1:]:
        # Compare headers (case-insensitive and trimmed)
        norm_curr = normalize_header(current.headers)
        norm_next = normalize_header(next_table.headers)

        if norm_curr == norm_next and len(norm_curr) > 0:
            # Concatenate rows
            new_rows = list(current.rows) + list(next_table.rows)
            new_cells = list(current.cells) + list(next_table.cells)
            current = TableData(
                headers=current.headers,
                rows=new_rows,
                page_number=current.page_number,
                cells=new_cells,
                confidence=min(current.confidence, next_table.confidence),
                title=current.title,
                metadata=current.metadata,
            )
        else:
            merged.append(current)
            current = next_table

    merged.append(current)
    return merged
