from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import VlmPipelineOptions, VlmConvertOptions
from docling.datamodel.vlm_engine_options import ApiVlmEngineOptions, VlmEngineType
from docling.pipeline.vlm_pipeline import VlmPipeline
from pharmaocr.config import DEFAULT_CONFIG, ModelConfig

def create_converter(config: ModelConfig) -> DocumentConverter:
    if config.use_ollama:
        engine_options = ApiVlmEngineOptions(engine_type=VlmEngineType.API_OLLAMA, timeout=300.0)
        vlm_options = VlmConvertOptions.from_preset(config.preset, engine_options=engine_options)
    else:
        vlm_options = VlmConvertOptions.from_preset(config.preset)


    pipeline_options = VlmPipelineOptions(
        vlm_options = vlm_options,
        enable_remote_services = config.use_ollama
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
