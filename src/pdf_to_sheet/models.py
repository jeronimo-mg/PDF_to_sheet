"""Core data models and abstract extractor interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Cell:
    """Represents an individual table cell."""
    content: str
    row_idx: int
    col_idx: int
    confidence: float = 1.0
    is_header: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TableData:
    """Represents a structured table extracted from a document page."""
    headers: list[str]
    rows: list[list[str]]
    page_number: int
    cells: list[Cell] = field(default_factory=list)
    confidence: float = 1.0
    title: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def row_count(self) -> int:
        return len(self.rows)

    @property
    def col_count(self) -> int:
        return len(self.headers) if self.headers else (len(self.rows[0]) if self.rows else 0)


@dataclass
class ExtractionResult:
    """Represents the complete result of a PDF extraction operation."""
    source_file: str
    tables: list[TableData]
    extractor_used: str
    success: bool
    warnings: list[str] = field(default_factory=list)
    execution_time_seconds: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseExtractor(ABC):
    """Abstract base class for table extraction strategies."""

    @abstractmethod
    def extract_tables(self, pdf_path: str, profile: str = "auto") -> ExtractionResult:
        """Extract tables from the specified PDF file using the given profile."""

