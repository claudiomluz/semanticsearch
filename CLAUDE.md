# CLAUDE.md — Semantic Search POC

Projeto experimental de aprendizado sobre busca semântica com banco vetorial e RAG.

## Ambiente
- Python 3.13 em `venv/`. Sempre usar `./venv/bin/python` e `./venv/bin/pip`.
- Ollama local rodando com modelo `qwen2.5:3b`.
- Tudo local e grátis — sem chaves de API.

## Comandos
- Instalar: `./venv/bin/pip install -r requirements.txt`
- Indexar: `./venv/bin/python src/ingest.py`
- Busca CLI: `./venv/bin/python src/search.py "query"`
- RAG CLI: `./venv/bin/python src/rag.py "query"`
- UI: `./venv/bin/streamlit run src/app.py`

## Arquitetura
- `src/config.py` centraliza parâmetros. Mudar modelo/dataset/top-k aqui.
- `src/db.py` carrega embedding e ChromaDB uma vez (lru_cache).
- Indexação é idempotente: `ingest.py` recria a coleção do zero.
- Similaridade exibida = 1 - distância cosseno.

## Convenções
- Responder em português brasileiro, direto.
- Manter STATUS.md atualizado ao fim de sessões com trabalho relevante.
