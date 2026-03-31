from pharmaocr.engine import create_converter, convert_pdf, DEFAULT_CONFIG
from pathlib import Path
from pharmaocr.scoring import build_document_result
import time

project_root = Path(__file__).parent
pdf_path = project_root / "ressources" / "Cite Medicale Villeray 2.pdf"

start  = time.time()
converter = create_converter(DEFAULT_CONFIG)
result = convert_pdf(str(pdf_path), converter)
extracted_text = result.document.export_to_markdown()
document_result = build_document_result(conv_result=result, filename="Test1.pdf")
print(document_result.markdown)
for page in document_result.pages:
    print(f"Page {page.page_number}: confidence={page.confidence}, grade={page.grade}")

end = time.time()
print(f"Processing time: {end - start} seconds")

