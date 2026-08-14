"""Hybrid table extractor orchestrating rule-based parsing with local AI vision fallback."""

import logging
import time

from pdf_to_sheet.extractors.local_ai import LocalAIExtractor, check_ollama_status
from pdf_to_sheet.extractors.rule_based import RuleBasedExtractor
from pdf_to_sheet.merger import merge_tables
from pdf_to_sheet.models import BaseExtractor, ExtractionResult

logger = logging.getLogger(__name__)


class HybridTableExtractor(BaseExtractor):
    """Orchestrater strategy: tries RuleBasedExtractor first, falls back to LocalAIExtractor if empty/low confidence."""

    def __init__(self, ollama_host: str = "http://localhost:11434") -> None:
        self.rule_extractor = RuleBasedExtractor()
        self.ai_extractor = LocalAIExtractor(host=ollama_host)
        self.ollama_host = ollama_host

    def extract_tables(self, pdf_path: str, profile: str = "generic") -> ExtractionResult:
        start_time = time.time()
        warnings: list[str] = []

        # Tier 1: Deterministic Rule-Based Extraction
        rule_result = self.rule_extractor.extract_tables(pdf_path, profile=profile)
        tables = rule_result.tables

        # Check if Tier 1 provided satisfactory tables
        is_satisfactory = len(tables) > 0 and any(t.row_count > 0 for t in tables)

        if not is_satisfactory:
            logger.info("Rule-based extraction returned low confidence/no tables. Attempting local AI vision fallback...")
            if check_ollama_status(self.ollama_host):
                ai_result = self.ai_extractor.extract_tables(pdf_path, profile=profile)
                if ai_result.tables:
                    tables = ai_result.tables
                    warnings.append("Used Local AI Vision fallback extraction.")
                else:
                    warnings.extend(ai_result.warnings)
            else:
                warnings.append(f"Rule-based extraction gave low confidence and Ollama AI service at {self.ollama_host} is offline.")
        else:
            # Merge multi-page continuous tables
            tables = merge_tables(tables)

        elapsed = time.time() - start_time
        return ExtractionResult(
            source_file=pdf_path,
            tables=tables,
            extractor_used="HybridTableExtractor",
            success=(len(tables) > 0),
            warnings=rule_result.warnings + warnings,
            execution_time_seconds=elapsed,
        )
