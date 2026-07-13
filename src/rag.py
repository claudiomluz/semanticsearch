"""RAG (caminho conversacional).

Query -> busca semântica -> monta prompt com trechos -> LLM local (Ollama) -> resposta.
"""
import ollama

from config import OLLAMA_MODEL, TOP_K
from i18n import LANG_NAME
from search import search

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions using ONLY the provided "
    "news excerpts. If the answer is not in the excerpts, say you don't know. "
    "Cite the article titles you used. Always answer in {language}."
)


def build_context(chunks: list[dict]) -> str:
    parts = []
    for i, c in enumerate(chunks, 1):
        parts.append(f"[{i}] Title: {c['title']} (Category: {c['category']})\n{c['text']}")
    return "\n\n".join(parts)


def answer(query: str, top_k: int = TOP_K, lang: str = "en") -> dict:
    """Recupera trechos, gera resposta do LLM e retorna resposta + fontes.

    lang: idioma da resposta ("pt" ou "en").
    """
    chunks = search(query, top_k=top_k)
    context = build_context(chunks)
    lang_name = LANG_NAME.get(lang, "English")
    user_msg = (
        f"News excerpts:\n\n{context}\n\n"
        f"Question: {query}\n\n"
        f"Answer based only on the excerpts above. "
        f"Write your entire answer in {lang_name}, regardless of the language "
        f"of the question or the excerpts."
    )
    resp = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system",
             "content": SYSTEM_PROMPT.format(language=LANG_NAME.get(lang, "English"))},
            {"role": "user", "content": user_msg},
        ],
    )
    return {"answer": resp["message"]["content"], "sources": chunks}


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "What happened in the technology sector?"
    result = answer(q)
    print(result["answer"])
    print("\n--- Fontes ---")
    for i, s in enumerate(result["sources"], 1):
        print(f"[{i}] {s['title']} ({s['category']}) score={s['score']}")
