# PharmaOCR

> Streamlit app that extracts text from pharmaceutical PDFs using a local vision-language model (IBM Granite-Docling 258M) running on Ollama.

## 🎯 Objective

Pharmaceutical documents (prescriptions, labels, package inserts) are often scanned PDFs whose text is locked inside images. PharmaOCR runs a small, locally-hosted VLM end-to-end on those PDFs — no cloud calls, no API keys — and returns clean, page-aware markdown plus a confidence panel so a reviewer can quickly spot pages that need re-OCR.

## 🏗️ Architecture

*PDF flows through Docling's VLM pipeline; Granite-Docling runs locally via Ollama; a deduplication pass strips repeated-line hallucinations before rendering.*

```mermaid
flowchart LR
    A[PDF Upload<br/>Streamlit] --> B[Docling<br/>DocumentConverter]
    B --> C[Granite-Docling 258M<br/>via Ollama]
    C --> D[Per-Page Text<br/>Extraction]
    D --> E[Dedup Filter<br/>repeated lines]
    E --> F[Markdown + Per-Page<br/>Confidence Panel]
```

## 🛠️ Tech Stack

- **VLM**: [ibm-granite/granite-docling-258M](https://huggingface.co/ibm-granite/granite-docling-258M) — 258M-parameter vision-language model
- **OCR pipeline**: [Docling](https://github.com/docling-project/docling) `VlmPipeline` + `DocumentConverter`
- **Local runtime**: [Ollama](https://ollama.com) (default, faster CPU inference) — falls back to PyTorch + Transformers
- **Frontend**: Streamlit
- **Data models**: Pydantic

## 📊 Outcomes

- Extracts page-level markdown from multi-page pharmaceutical PDFs without sending data to any external API.
- Runs on CPU at usable latency thanks to Ollama (vs. the heavier PyTorch/Transformers path).
- Filters Granite-Docling's most common failure mode (repeating the same line many times in a row) via a simple counter-based dedup pass in `pharmaocr/scoring.py`.

> No formal accuracy benchmark has been committed yet — see *Limitations*.

## 📁 Repository Structure

```
PharmaOCR/
├── main.py                      # Streamlit entry point + 4-step progress UI
├── pharmaocr/
│   ├── config.py                # ModelConfig (preset + ollama toggle)
│   ├── engine.py                # Builds DocumentConverter w/ VlmPipeline
│   ├── scoring.py               # Dedup + (placeholder) confidence grading
│   ├── models.py                # Pydantic: PageResult, DocumentResult
│   └── ui/components.py         # Streamlit upload / results / confidence panel
├── test_pipeline.py             # Headless smoke test against a local PDF
└── requirements.txt
```

## 🚀 How to Run

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r requirements.txt

# Pull the model into Ollama (one-time)
ollama pull ibm/granite-docling:258m

streamlit run main.py
```

To bypass Ollama and run on PyTorch/Transformers directly, set `use_ollama=False` in [pharmaocr/config.py](pharmaocr/config.py).

## 📝 Limitations

- **Confidence scoring is currently a placeholder.** `pharmaocr/scoring.py` returns `confidence=0.0` / `grade=POOR` for every page. The UI panel is wired up but not yet meaningful — implementing real per-page confidence (e.g. from VLM token logprobs) is the next planned step.
- **Hallucination filter is line-exact, not semantic.** It catches Granite-Docling's stutter pattern (same line repeated 3+ times) but won't flag plausible-but-wrong extractions.
- **No committed benchmark.** Sample PDFs live under `ressources/` (gitignored). Adding a small public test set with ground-truth markdown is the right next move before claiming accuracy numbers.
- **Local-only.** No cloud deployment — by design, since pharma documents are often sensitive — but it does mean each user needs Ollama installed.
