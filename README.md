# PharmaOCR

Streamlit app for extracting text from pharmaceutical PDF documents using IBM Granite-Docling 258M.

## Features

- PDF upload via web interface
- OCR extraction powered by Granite-Docling (258M parameters)
- Per-page text extraction with confidence scoring
- Hallucination detection (repeated line filtering)
- Processing time tracking with step-by-step progress bar
- GPU cloud inference via Google Colab + Cloudflare tunnel

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

### Option A: Local Ollama (CPU)

1. Download and install [Ollama](https://ollama.com/download/windows)
2. Pull the model:
   ```bash
   ollama pull ibm/granite-docling:258m
   ```
3. Ollama runs as a background service on `localhost:11434`
4. In `pharmaocr/config.py`, set:
   ```python
   ollama_url = "http://localhost:11434/v1/chat/completions"
   ```

### Option B: GPU Cloud via Google Colab (recommended)

Runs the model on a free T4 GPU for faster inference (~10s vs ~13s local CPU).

#### On Google Colab

1. Create a new notebook at [colab.research.google.com](https://colab.research.google.com)
2. Enable GPU: **Runtime > Change runtime type > T4 GPU > Save**
3. Run the following cells in order:

**Cell 1 — Install dependencies and Ollama**
```bash
!apt-get install -y zstd
!curl -fsSL https://ollama.com/install.sh | sh
```

**Cell 2 — Start Ollama server**
```bash
!OLLAMA_ORIGINS="*" OLLAMA_HOST=0.0.0.0:11434 nohup ollama serve > ollama.log 2>&1 &
!sleep 5
```
- `OLLAMA_ORIGINS="*"` allows requests from any origin (prevents 403 errors)
- `OLLAMA_HOST=0.0.0.0:11434` listens on all network interfaces

**Cell 3 — Download the model**
```bash
!ollama pull ibm/granite-docling:258m
```

**Cell 4 — Verify Ollama is running**
```bash
!curl http://localhost:11434/api/tags
```
Should return JSON with `ibm/granite-docling:258m` listed.

**Cell 5 — Create the Cloudflare tunnel**
```bash
!wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
!chmod +x cloudflared
!nohup ./cloudflared tunnel --url http://localhost:11434 > tunnel.log 2>&1 &
!sleep 10
!grep -o 'https://.*trycloudflare.com' tunnel.log
```
Copy the printed URL (e.g. `https://xxx.trycloudflare.com`).

**Cell 6 — Verify the tunnel**
```python
import requests
r = requests.get("https://YOUR_URL.trycloudflare.com/api/tags")
print(r.status_code, r.text)
```
Should return `200` with the model list.

#### On your local machine (VS Code)

1. Update `ollama_url` in `pharmaocr/config.py`:
   ```python
   ollama_url = "https://YOUR_URL.trycloudflare.com/v1/chat/completions"
   ```
2. The URL changes every Colab session — update it each time.

To disable Ollama and use PyTorch/Transformers instead, set `use_ollama=False` in `pharmaocr/config.py`.

> **Note:** Free Colab sessions expire after a few hours of inactivity. When that happens, re-run all cells (1-6) and update the URL.

## Run

```bash
streamlit run main.py
```

## Tech Stack

- **Model**: [ibm-granite/granite-docling-258M](https://huggingface.co/ibm-granite/granite-docling-258M)
- **Pipeline**: [Docling](https://github.com/docling-project/docling) VLM pipeline
- **Frontend**: Streamlit
- **Runtime**: [Ollama](https://ollama.com) via Google Colab T4 GPU or local CPU
