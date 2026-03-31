import streamlit as st
from pharmaocr.models import DocumentResult


def render_upload_section():
    st.title("PharmaOCR - Document Analysis")
    st.write("Upload your pharmaceutical documents for analysis.")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf"])
    return uploaded_file


def render_results(result: DocumentResult):
    st.subheader("Extracted Text")
    for page in result.pages:
        st.markdown(f"**Page {page.page_number}**")
        st.text_area(f"Page {page.page_number}", value=page.text, height=200)
    with st.expander("Full Markdown Export"):
        st.markdown(result.markdown)


def render_confidence_panel(result: DocumentResult):
    st.subheader("Confidence Scores")
    for page in result.pages:
        st.write(f"**Page {page.page_number}:** {page.confidence:.2f} — {page.grade.value}")
