"""Configuração central compartilhada entre os módulos."""
from pathlib import Path

# Caminho de persistência do ChromaDB
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = str(PROJECT_ROOT / "data" / "chroma")
COLLECTION_NAME = "news"

# Modelo de embedding (local, 384 dims, inglês)
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Dataset HuggingFace. "bbc" (~2k artigos, leve) ou "ag_news" (~120k).
DATASET = "bbc"

# LLM local via Ollama para o caminho conversacional (RAG)
OLLAMA_MODEL = "qwen2.5:3b"

# Quantos vizinhos recuperar por padrão
TOP_K = 5
