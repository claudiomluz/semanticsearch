"""Interface Streamlit: usuário escolhe entre Busca (estruturada) ou Chat (RAG).

Rodar:  streamlit run src/app.py
"""
import streamlit as st

from config import DATASET, OLLAMA_MODEL, TOP_K
from search import search
from rag import answer

st.set_page_config(page_title="Semantic Search POC", page_icon="🔎")
st.title("🔎 Semantic Search + RAG")
st.caption(f"Dataset: {DATASET} · Embedding: MiniLM · LLM: {OLLAMA_MODEL}")

mode = st.radio(
    "Modo de interação",
    ["Busca (estruturada)", "Chat (conversacional)"],
    horizontal=True,
)
top_k = st.slider("Resultados a recuperar (top-K)", 1, 10, TOP_K)
query = st.text_input("Sua consulta", placeholder="ex: technology company earnings")

if query:
    if mode.startswith("Busca"):
        with st.spinner("Buscando..."):
            results = search(query, top_k=top_k)
        st.subheader(f"{len(results)} resultados")
        for i, r in enumerate(results, 1):
            with st.container(border=True):
                st.markdown(f"**{i}. {r['title']}**")
                cols = st.columns(2)
                cols[0].metric("Categoria", r["category"])
                cols[1].metric("Similaridade", r["score"])
                st.write(r["snippet"])
    else:
        with st.spinner("Recuperando + gerando resposta (LLM local)..."):
            result = answer(query, top_k=top_k)
        st.subheader("Resposta")
        st.write(result["answer"])
        with st.expander("Trechos-fonte usados"):
            for i, s in enumerate(result["sources"], 1):
                st.markdown(
                    f"**[{i}] {s['title']}** · {s['category']} · score={s['score']}"
                )
                st.write(s["snippet"])
