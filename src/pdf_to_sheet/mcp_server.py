"""Local MCP (Model Context Protocol) server interface for Desktop Commander & local Ollama integration."""

import json
import logging
import os
import sys
from typing import Any

from pdf_to_sheet.extractors.hybrid import HybridTableExtractor
from pdf_to_sheet.writers.excel import ExcelWriter

logger = logging.getLogger(__name__)


def inspect_pdf_tables_handler(pdf_path: str) -> dict[str, Any]:
    """Inspect PDF file structures and extract table metadata."""
    if not os.path.exists(pdf_path):
        return {"success": False, "error": f"File not found: {pdf_path}"}

    extractor = HybridTableExtractor()
    result = extractor.extract_tables(pdf_path)

    table_summaries = []
    for idx, t in enumerate(result.tables, start=1):
        table_summaries.append({
            "table_id": idx,
            "page_number": t.page_number,
            "headers": t.headers,
            "row_count": len(t.rows),
        })

    return {
        "success": True,
        "pdf_path": pdf_path,
        "page_count": max((t.page_number for t in result.tables), default=0),
        "tables_count": len(result.tables),
        "tables": table_summaries,
    }


def convert_pdf_handler(pdf_path: str, output_path: str) -> dict[str, Any]:
    """Convert a single PDF to a formatted Excel workbook."""
    if not os.path.exists(pdf_path):
        return {"success": False, "error": f"File not found: {pdf_path}"}

    extractor = HybridTableExtractor()
    result = extractor.extract_tables(pdf_path)

    writer = ExcelWriter()
    generated_path = writer.write(result, output_path)

    return {
        "success": True,
        "source_file": pdf_path,
        "output_file": generated_path,
        "tables_extracted": len(result.tables),
        "execution_time_seconds": result.execution_time_seconds,
    }


def batch_convert_dir_handler(input_dir: str, output_dir: str) -> dict[str, Any]:
    """Batch convert all PDF files in a directory to formatted Excel workbooks."""
    if not os.path.isdir(input_dir):
        return {"success": False, "error": f"Directory not found: {input_dir}"}

    os.makedirs(output_dir, exist_ok=True)
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    converted = []

    for fname in pdf_files:
        src = os.path.join(input_dir, fname)
        out_name = os.path.splitext(fname)[0] + ".xlsx"
        dest = os.path.join(output_dir, out_name)

        res = convert_pdf_handler(src, dest)
        if res.get("success"):
            converted.append(dest)

    return {
        "success": True,
        "input_dir": input_dir,
        "output_dir": output_dir,
        "total_files": len(pdf_files),
        "converted_files": converted,
    }


def handle_mcp_tool_call(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Dispatch MCP tool calls for Desktop Commander."""
    try:
        if tool_name == "inspect_pdf_tables":
            pdf_path = arguments.get("pdf_path", "")
            return inspect_pdf_tables_handler(pdf_path)

        if tool_name == "convert_pdf":
            pdf_path = arguments.get("pdf_path", "")
            output_path = arguments.get("output_path", "")
            return convert_pdf_handler(pdf_path, output_path)

        if tool_name == "batch_convert_dir":
            input_dir = arguments.get("input_dir", "")
            output_dir = arguments.get("output_dir", "")
            return batch_convert_dir_handler(input_dir, output_dir)

        return {"success": False, "error": f"Unknown tool: {tool_name}"}
    except Exception as exc:  # noqa: BLE001
        logger.error("MCP tool call error (%s): %s", tool_name, exc)
        return {"success": False, "error": str(exc)}


def main() -> None:
    """Stdio entrypoint for MCP JSON-RPC server execution."""
    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        print("pdf-to-sheet MCP Server v0.1.0")
        sys.exit(0)

    # Simple stdio listener for JSON-RPC MCP calls
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            tool_name = req.get("tool", req.get("name", ""))
            arguments = req.get("arguments", req.get("params", {}))
            res = handle_mcp_tool_call(tool_name, arguments)
            response = {"id": req.get("id", 1), "result": res}
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
        except Exception as exc:  # noqa: BLE001
            sys.stdout.write(json.dumps({"error": str(exc)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
