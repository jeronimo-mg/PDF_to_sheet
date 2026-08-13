"""Unit tests for RuleBasedExtractor engine."""

import os

from pdf_to_sheet.extractors.rule_based import RuleBasedExtractor
from pdf_to_sheet.models import ExtractionResult


def test_rule_based_extractor_on_sample_le() -> None:
    sample_pdf = "R11.01-2151-LE-0001_2.pdf"
    assert os.path.exists(sample_pdf), f"Sample PDF {sample_pdf} not found"

    extractor = RuleBasedExtractor()
    result = extractor.extract_tables(sample_pdf)

    assert isinstance(result, ExtractionResult)
    assert result.source_file == sample_pdf
    assert result.success is True
    assert len(result.tables) > 0

    first_table = result.tables[0]
    assert first_table.row_count > 0
    assert first_table.col_count > 0


def test_rule_based_extractor_on_sample_li() -> None:
    sample_pdf = "R11.01-2151-LI-0001_3-1.pdf"
    assert os.path.exists(sample_pdf), f"Sample PDF {sample_pdf} not found"

    extractor = RuleBasedExtractor()
    result = extractor.extract_tables(sample_pdf)

    assert isinstance(result, ExtractionResult)
    assert result.source_file == sample_pdf
    assert result.success is True
    assert len(result.tables) > 0
