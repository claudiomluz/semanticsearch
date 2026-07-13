"""Busca semântica pura (caminho estruturado).

Query -> embedding -> ChromaDB top-K -> resultados com metadata e score.
"""
from config import TOP_K
from db import get_collection, embed


def search(query: str, top_k: int = TOP_K) -> list[dict]:
    """Retorna os top-K chunks mais próximos com título, categoria e score."""
    col = get_collection()
    res = col.query(
        query_embeddings=embed([query]),
        n_results=top_k,
    )
    out = []
    docs = res["documents"][0]
    metas = res["metadatas"][0]
    dists = res["distances"][0]
    for doc, meta, dist in zip(docs, metas, dists):
        out.append({
            "title": meta.get("title", ""),
            "category": meta.get("category", ""),
            # distância cosseno -> similaridade (1 = idêntico)
            "score": round(1 - dist, 4),
            "snippet": doc[:300] + ("..." if len(doc) > 300 else ""),
            "text": doc,
        })
    return out


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "technology company profits"
    for i, r in enumerate(search(q), 1):
        print(f"{i}. [{r['category']}] {r['title']}  (score={r['score']})")
        print(f"   {r['snippet']}\n")
