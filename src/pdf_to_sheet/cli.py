"""Command Line Interface (CLI) entrypoint with Rich terminal progress and audit logging."""

import logging
import os
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn

from pdf_to_sheet.extractors.hybrid import HybridTableExtractor
from pdf_to_sheet.writers.excel import ExcelWriter

console = Console()


logger = logging.getLogger(__name__)


def setup_logging(log_dir: str = "logs") -> str:
    """Setup file logger."""
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "conversion.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    return log_file


def open_file_dialog() -> str | None:
    """Open a native GUI file picker for PDF selection."""
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        file_path = filedialog.askopenfilename(
            title="Selecione o arquivo PDF para converter",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")],
        )
        root.destroy()
        return file_path if file_path else None
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to open GUI file dialog: %s", exc)
        return None


@click.command()
@click.option("--file", "-f", "pdf_file", type=click.Path(exists=True), help="Path to a single input PDF file.")
@click.option("--dir", "-d", "pdf_dir", type=click.Path(exists=True), help="Path to directory containing PDF files for batch processing.")
@click.option("--output", "-o", "output_path", type=click.Path(), help="Output XLSX file path or directory.")
@click.option("--profile", "-p", default="auto", type=click.Choice(["auto", "generic", "le_li"], case_sensitive=False), help="Table extraction profile (auto, generic, or le_li).")
@click.option("--gui", is_flag=True, help="Open native Windows GUI file selection dialog.")
@click.option("--ollama-host", default="http://localhost:11434", help="Host URL for local Ollama service.")
def main(pdf_file: str | None, pdf_dir: str | None, output_path: str | None, profile: str, gui: bool, ollama_host: str) -> None:
    """Convert PDF tables into Excel XLSX spreadsheets with hybrid rule-based and local AI vision extraction."""
    if gui or (not pdf_file and not pdf_dir):
        selected = open_file_dialog()
        if selected:
            pdf_file = selected
        else:
            if not pdf_file and not pdf_dir:
                console.print("[yellow]Nenhum arquivo PDF foi selecionado.[/yellow]")
                sys.exit(0)

    log_file = setup_logging()
    logger.info("CLI execution started. File=%s, Dir=%s, Profile=%s", pdf_file, pdf_dir, profile)

    console.print(Panel(f"[bold blue]PDF to Sheet Converter[/bold blue]\n[dim]Privacy-focused local PDF table extraction (Profile: [cyan]{profile}[/cyan])[/dim]", expand=False))

    pdf_files: list[str] = []
    if pdf_file:
        pdf_files.append(pdf_file)
    if pdf_dir:
        for root, _, files in os.walk(pdf_dir):
            for fname in files:
                if fname.lower().endswith(".pdf"):
                    pdf_files.append(os.path.join(root, fname))

    if not pdf_files:
        console.print("[yellow]No PDF files found to process.[/yellow]")
        sys.exit(0)

    extractor = HybridTableExtractor(ollama_host=ollama_host)
    writer = ExcelWriter()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[green]Converting PDFs...", total=len(pdf_files))

        for pdf_path in pdf_files:
            filename = os.path.basename(pdf_path)
            progress.update(task, description=f"[cyan]Parsing {filename}...[/cyan]")

            # Determine output file path
            if output_path:
                if output_path.lower().endswith(".xlsx"):
                    dest_xlsx = output_path
                else:
                    dest_xlsx = os.path.join(output_path, f"{os.path.splitext(filename)[0]}.xlsx")
            else:
                dest_xlsx = f"{os.path.splitext(pdf_path)[0]}.xlsx"

            result = extractor.extract_tables(pdf_path, profile=profile)
            if result.success and result.tables:
                writer.write(result, dest_xlsx)
                logger.info("Successfully converted %s -> %s (%d tables)", pdf_path, dest_xlsx, len(result.tables))
                console.print(f" [bold green][OK][/bold green] Converted: [bold]{filename}[/bold] -> [cyan]{dest_xlsx}[/cyan] ({len(result.tables)} table(s))")

                # Auto-open generated spreadsheet on Windows when run interactively
                if hasattr(os, "startfile") and (gui or len(pdf_files) == 1):
                    try:
                        os.startfile(os.path.abspath(dest_xlsx))
                    except Exception as exc:  # noqa: BLE001
                        logger.warning("Could not auto-open spreadsheet: %s", exc)
            else:
                logger.warning("Failed to extract tables from %s. Warnings: %s", pdf_path, result.warnings)
                console.print(f" [bold red][WARN][/bold red] Warnings for [bold]{filename}[/bold]: {', '.join(result.warnings)}")

            progress.advance(task)

    console.print(f"\n[bold green]Execution completed![/bold green] Logs stored in [dim]{log_file}[/dim]")


if __name__ == "__main__":
    main()
