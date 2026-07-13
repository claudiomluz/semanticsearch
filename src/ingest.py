"""Indexação: baixa dataset, quebra em chunks, gera embeddings e popula o ChromaDB.

Uso:
    python src/ingest.py            # usa DATASET do config, todos os artigos
    python src/ingest.py --limit 500
    python src/ingest.py --dataset ag_news --limit 2000
"""
import argparse

from datasets import load_dataset

from config import DATASET, COLLECTION_NAME
from db import get_client, embed

# Mapa: nome curto -> (repo HuggingFace, coluna de texto, coluna de categoria)
DATASETS = {
    "bbc": ("SetFit/bbc-news", "text", "label_text"),
    "ag_news": ("ag_news", "text", None),  # label numérico, mapeado abaixo
}
AG_NEWS_LABELS = {0: "World", 1: "Sports", 2: "Business", 3: "Sci/Tech"}


def chunk_text(text: str, words_per_chunk: int = 180, overlap: int = 30) -> list[str]:
    """Quebra texto em pedaços por contagem de palavras, com sobreposição."""
    words = text.split()
    if len(words) <= words_per_chunk:
        return [text]
    chunks = []
    step = words_per_chunk - overlap
    for start in range(0, len(words), step):
        chunk = " ".join(words[start:start + words_per_chunk])
        if chunk:
            chunks.append(chunk)
        if start + words_per_chunk >= len(words):
            break
    return chunks


def category_for(name: str, row: dict, cat_col: str | None) -> str:
    if name == "ag_news":
        return AG_NEWS_LABELS.get(row.get("label"), "Unknown")
    return row.get(cat_col, "Unknown") if cat_col else "Unknown"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default=DATASET, choices=list(DATASETS))
    parser.add_argument("--limit", type=int, default=None, help="máx. de artigos")
    parser.add_argument("--batch", type=int, default=256)
    args = parser.parse_args()

    repo, text_col, cat_col = DATASETS[args.dataset]
    print(f"Baixando dataset '{repo}' ...")
    ds = load_dataset(repo, split="train")
    if args.limit:
        ds = ds.select(range(min(args.limit, len(ds))))
    print(f"{len(ds)} artigos carregados.")

    # Recria a coleção do zero para reindexação idempotente
    client = get_client()
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    col = client.get_or_create_collection(
        COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )

    ids, docs, metas = [], [], []

    def flush():
        if not docs:
            return
        col.add(ids=ids, documents=docs, embeddings=embed(docs), metadatas=metas)
        ids.clear(); docs.clear(); metas.clear()

    total_chunks = 0
    for art_idx, row in enumerate(ds):
        text = (row.get(text_col) or "").strip()
        if not text:
            continue
        title = text.split("\n", 1)[0][:120]
        category = category_for(args.dataset, row, cat_col)
        for c_idx, chunk in enumerate(chunk_text(text)):
            ids.append(f"{art_idx}-{c_idx}")
            docs.append(chunk)
            metas.append({
                "article_id": art_idx,
                "chunk": c_idx,
                "title": title,
                "category": category,
            })
            total_chunks += 1
            if len(docs) >= args.batch:
                flush()
                print(f"  indexados {total_chunks} chunks...", end="\r")
    flush()

    print(f"\nPronto. {total_chunks} chunks de {len(ds)} artigos em '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    main()
