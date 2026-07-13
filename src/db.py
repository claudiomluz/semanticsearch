"""Acesso ao ChromaDB e ao modelo de embedding (carregados uma vez)."""
from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer

from config import CHROMA_DIR, COLLECTION_NAME, EMBED_MODEL


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    """Carrega o modelo de embedding (cacheado no processo)."""
    return SentenceTransformer(EMBED_MODEL)


@lru_cache(maxsize=1)
def get_client() -> chromadb.ClientAPI:
    """Cliente ChromaDB persistente em disco."""
    return chromadb.PersistentClient(path=CHROMA_DIR)


def get_collection(create: bool = False):
    """Retorna a coleção de notícias. create=True cria se não existir."""
    client = get_client()
    if create:
        return client.get_or_create_collection(
            COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
        )
    return client.get_collection(COLLECTION_NAME)


def embed(texts: list[str]) -> list[list[float]]:
    """Gera embeddings para uma lista de textos."""
    model = get_model()
    return model.encode(texts, show_progress_bar=False).tolist()
