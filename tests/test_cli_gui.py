"""Unit tests for CLI GUI picker option."""

from click.testing import CliRunner

from pdf_to_sheet.cli import main


def test_cli_gui_flag_without_tkinter_dialog() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "--gui" in result.output
