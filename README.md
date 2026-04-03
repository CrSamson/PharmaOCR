# PharmaOCR

Streamlit app for extracting text from pharmaceutical PDF documents using IBM Granite Vision 2B.

## Features

- PDF upload via web interface
- OCR extraction powered by Granite 3.2 Vision (2B parameters)
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

### Ollama (recommended for faster CPU inference)

1. Download and install [Ollama](https://ollama.com/download/windows)
2. Pull the model:
   ```bash
   ollama pull granite3.2-vision:2b
   ```
3. Ollama runs as a background service on `localhost:11434`

To disable Ollama and use PyTorch/Transformers instead, set `use_ollama=False` in `pharmaocr/config.py`.

## Run

```bash
streamlit run main.py
```

## Tech Stack

- **Model**: [Granite 3.2 Vision 2B](https://huggingface.co/ibm-granite/granite-3.2-2b-vision-preview) via Ollama
- **Pipeline**: [Docling](https://github.com/docling-project/docling) VLM pipeline
- **Frontend**: Streamlit
- **Runtime**: [Ollama](https://ollama.com) (default) or PyTorch + Transformers
