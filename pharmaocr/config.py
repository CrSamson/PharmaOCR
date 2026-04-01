from dataclasses import dataclass

@dataclass
class ModelConfig:
    preset: str
    use_ollama: bool = False

DEFAULT_CONFIG = ModelConfig(
    preset = "granite_docling",
    use_ollama = True
)
