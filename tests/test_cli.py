"""CLI unit tests using Click CliRunner."""

import os

from typing import Any

from click.testing import CliRunner

from pdf_to_sheet.cli import main


def test_cli_help() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Convert PDF tables into Excel XLSX spreadsheets" in result.output


def test_cli_single_file_conversion(tmp_path: Any) -> None:
    runner = CliRunner()
    sample_pdf = "R11.01-2151-LE-0001_2.pdf"
    out_xlsx = str(tmp_path / "le_output.xlsx")

    result = runner.invoke(main, ["--file", sample_pdf, "--output", out_xlsx, "--profile", "le_li"])
    assert result.exit_code == 0
    assert os.path.exists(out_xlsx)


def test_cli_profile_help() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "--profile" in result.output
    assert "[generic|le_li]" in result.output

