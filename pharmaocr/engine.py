from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import VlmPipelineOptions, VlmConvertOptions
from docling.pipeline.vlm_pipeline import VlmPipeline
from pharmaocr.config import DEFAULT_CONFIG, ModelConfig

def create_converter(config: ModelConfig) -> DocumentConverter:
    vlm_options = VlmConvertOptions.from_preset(config.preset)
    vlm_options.scale = 1.0

    pipeline_options = VlmPipelineOptions(
        vlm_options = vlm_options
    )
    converter = DocumentConverter(
        format_options = {
            InputFormat.PDF: PdfFormatOption(
                pipeline_cls = VlmPipeline,
                pipeline_options = pipeline_options
            )
        }
    )
    return converter

def convert_pdf(pdf_path: str, converter: DocumentConverter):
    result = converter.convert(source=pdf_path)
    return result
