"""Unit tests for Desktop Commander compatible MCP server module."""

import os

from pdf_to_sheet.mcp_server import handle_mcp_tool_call


def test_mcp_inspect_pdf_tables(tmp_path) -> None:
    sample_pdf = "R11.01-2151-LE-0001_2.pdf"
    if not os.path.exists(sample_pdf):
        return

    result = handle_mcp_tool_call("inspect_pdf_tables", {"pdf_path": sample_pdf})
    assert result["success"] is True
    assert result["page_count"] == 2
    assert "tables" in result


def test_mcp_convert_pdf_tool(tmp_path) -> None:
    sample_pdf = "R11.01-2151-LE-0001_2.pdf"
    if not os.path.exists(sample_pdf):
        return

    output_xlsx = str(tmp_path / "mcp_out.xlsx")
    result = handle_mcp_tool_call("convert_pdf", {"pdf_path": sample_pdf, "output_path": output_xlsx})
    assert result["success"] is True
    assert os.path.exists(output_xlsx)


def test_mcp_unknown_tool() -> None:
    result = handle_mcp_tool_call("invalid_tool_name", {})
    assert result["success"] is False
    assert "Unknown tool" in result["error"]
