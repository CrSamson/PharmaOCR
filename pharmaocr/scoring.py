from collections import Counter
from pharmaocr.models import ConfidenceGrade, DocumentResult, PageResult

MAX_REPEATS = 2


def deduplicate_lines(lines: list[str]) -> list[str]:
    counts = Counter(lines)
    seen = Counter()
    result = []
    for line in lines:
        seen[line] += 1
        if counts[line] <= MAX_REPEATS or seen[line] <= MAX_REPEATS:
            result.append(line)
    return result


def assign_grade(confidence: float) -> ConfidenceGrade:
    if confidence < 0.25:
        return ConfidenceGrade.POOR
    elif confidence < 0.5:
        return ConfidenceGrade.FAIR
    elif confidence < 0.75:
        return ConfidenceGrade.GOOD
    else:
        return ConfidenceGrade.EXCELLENT


def build_document_result(conv_result, filename: str) -> DocumentResult:
    doc = conv_result.document
    markdown = doc.export_to_markdown()
    raw_dict = doc.export_to_dict()

    page_texts = {}
    for item, _level in doc.iterate_items():
        if hasattr(item, 'text') and item.text:
            prov = item.prov[0] if hasattr(item, 'prov') and item.prov else None
            page_no = prov.page_no if prov and hasattr(prov, 'page_no') else 0
            page_texts.setdefault(page_no, []).append(item.text)

    pages = []
    for page_no in sorted(page_texts.keys()):
        cleaned = deduplicate_lines(page_texts[page_no])
        text = "\n".join(cleaned)
        pages.append(PageResult(
            page_number=page_no,
            text=text,
            confidence=0.0,
            grade=ConfidenceGrade.POOR,
        ))

    return DocumentResult(
        filename=filename,
        pages=pages,
        markdown=markdown,
        raw_dict=raw_dict,
    )
