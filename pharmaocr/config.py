from dataclasses import dataclass

@dataclass
class ModelConfig:
    preset: str
    use_ollama: bool = False
    ollama_url: str = "http://localhost:11434/v1/chat/completions"

DEFAULT_CONFIG = ModelConfig(
    preset = "granite_docling",
    use_ollama = True,
    ollama_url = "https://had-straight-clusters-broadway.trycloudflare.com/v1/chat/completions"
)
