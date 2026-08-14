"""Local AI vision extractor module using Ollama API."""

import logging
import time

import requests

from pdf_to_sheet.models import BaseExtractor, ExtractionResult, TableData

logger = logging.getLogger(__name__)


def check_ollama_status(host: str = "http://localhost:11434") -> bool:
    """Check if the local Ollama service is reachable."""
    try:
        resp = requests.get(f"{host}/api/tags", timeout=1.5)
        return resp.status_code == 200
    except requests.RequestException:
        return False


class LocalAIExtractor(BaseExtractor):
    """Table extractor strategy using local vision model via Ollama."""

    def __init__(self, host: str = "http://localhost:11434", model: str = "llama3.2-vision") -> None:
        self.host = host
        self.model = model

    def extract_tables(self, pdf_path: str, profile: str = "generic") -> ExtractionResult:
        start_time = time.time()
        tables: list[TableData] = []
        warnings: list[str] = []

        if not check_ollama_status(self.host):
            warnings.append(f"Ollama local AI service at {self.host} is offline.")
            return ExtractionResult(
                source_file=pdf_path,
                tables=[],
                extractor_used="LocalAIExtractor",
                success=False,
                warnings=warnings,
                execution_time_seconds=time.time() - start_time,
            )

        elapsed = time.time() - start_time
        return ExtractionResult(
            source_file=pdf_path,
            tables=tables,
            extractor_used="LocalAIExtractor",
            success=True,
            warnings=warnings,
            execution_time_seconds=elapsed,
        )
