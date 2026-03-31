# PharmaOCR

Streamlit app for extracting text from pharmaceutical PDF documents using IBM Granite-Docling 258M.

## Features

- PDF upload via web interface
- OCR extraction powered by Granite-Docling (258M parameters)
- Per-page text extraction with confidence scoring
- Hallucination detection (repeated line filtering)
- Processing time tracking with step-by-step progress bar

## Project Structure

```
PharmaOCR/
├── main.py                  # Streamlit entry point
├── pharmaocr/
│   ├── config.py            # Model configuration
│   ├── engine.py            # DocumentConverter + VLM pipeline
│   ├── models.py            # Pydantic data models
│   ├── scoring.py           # Confidence scoring + deduplication
│   └── ui/
│       └── components.py    # Streamlit UI components
└── ressources/              # Sample PDFs
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

## Run

```bash
streamlit run main.py
```

## Tech Stack

- **Model**: [ibm-granite/granite-docling-258M](https://huggingface.co/ibm-granite/granite-docling-258M)
- **Pipeline**: [Docling](https://github.com/docling-project/docling) VLM pipeline
- **Frontend**: Streamlit
- **Runtime**: PyTorch + Transformers (CPU)
