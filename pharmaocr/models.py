from enum import Enum
from pydantic import BaseModel

class ConfidenceGrade(Enum):
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"

class PageResult(BaseModel):
    page_number: int
    text: str
    confidence: float
    grade: ConfidenceGrade

class DocumentResult(BaseModel):
    filename: str
    pages: list[PageResult]
    markdown: str
    raw_dict: dict