"""Internacionalização (i18n): strings da interface em português e inglês.

Uso:
    from i18n import t
    t("title", lang)   # -> string traduzida
"""

LANGUAGES = {"pt": "🇧🇷 PT", "en": "🇺🇸 EN"}
DEFAULT_LANG = "pt"

TRANSLATIONS = {
    "pt": {
        "title": "🔎 Busca Semântica + RAG",
        "caption": "Dataset: {dataset} · Embedding: MiniLM · LLM: {llm}",
        "help_button": "📖 Ajuda",
        "mode_label": "Modo de interação",
        "mode_search": "Busca (estruturada)",
        "mode_chat": "Chat (conversacional)",
        "topk_label": "Resultados a recuperar (top-K)",
        "query_label": "Sua consulta",
        "query_placeholder": "ex: technology company earnings",
        "searching": "Buscando...",
        "results_header": "{n} resultados",
        "category": "Categoria",
        "similarity": "Similaridade",
        "generating": "Recuperando + gerando resposta (LLM local)...",
        "answer_header": "Resposta",
        "sources_expander": "Trechos-fonte usados",
    },
    "en": {
        "title": "🔎 Semantic Search + RAG",
        "caption": "Dataset: {dataset} · Embedding: MiniLM · LLM: {llm}",
        "help_button": "📖 Help",
        "mode_label": "Interaction mode",
        "mode_search": "Search (structured)",
        "mode_chat": "Chat (conversational)",
        "topk_label": "Results to retrieve (top-K)",
        "query_label": "Your query",
        "query_placeholder": "e.g. technology company earnings",
        "searching": "Searching...",
        "results_header": "{n} results",
        "category": "Category",
        "similarity": "Similarity",
        "generating": "Retrieving + generating answer (local LLM)...",
        "answer_header": "Answer",
        "sources_expander": "Source excerpts used",
    },
}

# Nome do idioma por extenso, para instruir o LLM a responder no idioma certo
LANG_NAME = {"pt": "Portuguese (Brazil)", "en": "English"}


def t(key: str, lang: str = DEFAULT_LANG, **fmt) -> str:
    """Retorna a string traduzida para `key` no idioma `lang`, com formatação."""
    table = TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANG])
    text = table.get(key, TRANSLATIONS[DEFAULT_LANG].get(key, key))
    return text.format(**fmt) if fmt else text
