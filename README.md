PharmaOCR/
├── main.py                    # Streamlit entry point (~30 lines)
├── requirements.txt           # Updated with docling, streamlit
├── ressources/                # Sample PDFs (exists)
├── pharmaocr/
│   ├── __init__.py
│   ├── config.py              # ModelConfig dataclass, thresholds, constants
│   ├── models.py              # Pydantic models: PageResult, DocumentResult, ConfidenceGrade
│   ├── engine.py              # DocumentConverter setup, convert_pdf(), model caching
│   ├── scoring.py             # Confidence extraction, aggregation, filtering
│   └── ui/
│       ├── __init__.py
│       └── components.py      # Streamlit UI components (upload, results, confidence panel)