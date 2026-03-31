from dataclasses import dataclass

@dataclass
class ModelConfig:
    preset: str

DEFAULT_CONFIG = ModelConfig(
    preset = "granite_docling"
)
