"""Interface Streamlit: usuário escolhe entre Busca (estruturada) ou Chat (RAG).

Bilíngue (PT/EN) — idioma escolhido no seletor do topo da página.

Rodar:  streamlit run src/app.py
"""
import streamlit as st

from config import DATASET, OLLAMA_MODEL, TOP_K
from i18n import LANGUAGES, DEFAULT_LANG, t
from search import search
from rag import answer

st.set_page_config(page_title="Semantic Search POC", page_icon="🔎")

# --- Seletor de idioma no topo (canto direito) ---
top_l, top_r = st.columns([3, 1])
with top_r:
    lang = st.segmented_control(
        "lang",
        options=list(LANGUAGES),
        format_func=lambda c: LANGUAGES[c],
        default=DEFAULT_LANG,
        label_visibility="collapsed",
        key="lang",
    ) or DEFAULT_LANG

# --- Cabeçalho ---
header_l, header_r = st.columns([4, 1])
with header_l:
    st.title(t("title", lang))
    st.caption(t("caption", lang, dataset=DATASET, llm=OLLAMA_MODEL))
with header_r:
    st.link_button(
        t("help_button", lang), "/app/static/help.html", use_container_width=True
    )

# --- Controles ---
mode = st.radio(
    t("mode_label", lang),
    [t("mode_search", lang), t("mode_chat", lang)],
    horizontal=True,
)
top_k = st.slider(t("topk_label", lang), 1, 10, TOP_K)
query = st.text_input(t("query_label", lang), placeholder=t("query_placeholder", lang))

if query:
    if mode == t("mode_search", lang):
        with st.spinner(t("searching", lang)):
            results = search(query, top_k=top_k)
        st.subheader(t("results_header", lang, n=len(results)))
        for i, r in enumerate(results, 1):
            with st.container(border=True):
                st.markdown(f"**{i}. {r['title']}**")
                cols = st.columns(2)
                cols[0].metric(t("category", lang), r["category"])
                cols[1].metric(t("similarity", lang), r["score"])
                st.write(r["snippet"])
    else:
        with st.spinner(t("generating", lang)):
            result = answer(query, top_k=top_k, lang=lang)
        st.subheader(t("answer_header", lang))
        st.write(result["answer"])
        with st.expander(t("sources_expander", lang)):
            for i, s in enumerate(result["sources"], 1):
                st.markdown(
                    f"**[{i}] {s['title']}** · {s['category']} · score={s['score']}"
                )
                st.write(s["snippet"])
