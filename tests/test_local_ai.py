"""Tests for Ollama local service health check and PDF image preprocessor."""

from pdf_to_sheet.extractors.local_ai import LocalAIExtractor, check_ollama_status


def test_check_ollama_status_offline_graceful() -> None:
    # Service on invalid port should safely return False
    is_available = check_ollama_status("http://localhost:59999")
    assert is_available is False


def test_local_ai_extractor_initialization() -> None:
    extractor = LocalAIExtractor(host="http://localhost:11434")
    assert extractor.host == "http://localhost:11434"
