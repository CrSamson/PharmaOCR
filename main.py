import tempfile
import time
import streamlit as st
from pharmaocr.ui.components import render_upload_section, render_results, render_confidence_panel
from pharmaocr.engine import create_converter, convert_pdf
from pharmaocr.scoring import build_document_result
from pharmaocr.config import DEFAULT_CONFIG

st.set_page_config(page_title="PharmaOCR", layout="wide")

@st.cache_resource
def load_converter():
    return create_converter(DEFAULT_CONFIG)

converter = load_converter()
uploaded_file = render_upload_section()
if uploaded_file is not None:
    start = time.time()
    progress = st.progress(0)
    status = st.empty()

    status.code("[ STEP 1/4 ]  Reading file...", language="text")
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    progress.progress(10)

    status.code("[ STEP 2/4 ]  Loading model...", language="text")
    progress.progress(20)

    status.code("[ STEP 3/4 ]  Running OCR inference...", language="text")
    result = convert_pdf(tmp_path, converter)
    if not result or not result.document:
        st.error("OCR conversion failed — no document returned.")
        st.stop()
    markdown = result.document.export_to_markdown()
    if not markdown or not markdown.strip():
        st.warning("OCR returned empty text. The document may not be readable.")
    progress.progress(80)

    status.code("[ STEP 4/4 ]  Building results...", language="text")
    document_result = build_document_result(result, uploaded_file.name)
    if not document_result.pages:
        st.error("No pages extracted from the document.")
        st.stop()
    elapsed = time.time() - start
    progress.progress(100)

    status.code(f"[  DONE  ]  Processed in {elapsed:.1f}s", language="text")

    render_results(document_result)
    render_confidence_panel(document_result)