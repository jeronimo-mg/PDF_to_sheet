"""Tests for HybridTableExtractor fallback strategy."""

import os

from pdf_to_sheet.extractors.hybrid import HybridTableExtractor
from pdf_to_sheet.models import ExtractionResult


def test_hybrid_extractor_fallbacks_to_rule_based() -> None:
    sample_pdf = "R11.01-2151-LE-0001_2.pdf"
    assert os.path.exists(sample_pdf)

    extractor = HybridTableExtractor()
    result = extractor.extract_tables(sample_pdf)

    assert isinstance(result, ExtractionResult)
    assert result.success is True
    assert len(result.tables) > 0
