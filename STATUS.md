# STATUS — Semantic Search POC

> Última atualização: 2026-07-12

## Objetivo
POC de aprendizado sobre busca semântica com banco vetorial e RAG, indexando
artigos jornalísticos em inglês, com interface para busca estruturada ou chat.

## Fase atual
em desenvolvimento

## Feito recentemente
- [2026-07-12] Arquitetura definida e scaffold completo criado: config, db,
  ingest, search, rag, app (Streamlit). venv Python 3.13 criado.
- [2026-07-12] README, .gitignore, requirements.txt escritos.

## Em andamento
- Instalação das dependências (pip install -r requirements.txt).
- Pull do modelo Ollama llama3.2:1b.

## Próximos passos
1. `./venv/bin/pip install -r requirements.txt`
2. `ollama pull llama3.2:1b`
3. `./venv/bin/python src/ingest.py` (indexar bbc-news)
4. Testar `search.py` e `rag.py` via CLI, depois `streamlit run src/app.py`
5. Configurar git remote e primeiro commit.

## Bloqueios / decisões pendentes
- Nenhum. (torch precisa ter wheel para Python 3.13 — validar no pip install.)

## Notas de contexto
- Embedding: all-MiniLM-L6-v2 (384 dims, inglês). Banco: ChromaDB persistente
  em `data/chroma/` (git-ignored). LLM RAG: llama3.2:1b via Ollama.
- Dataset padrão: `SetFit/bbc-news` (~2k artigos, leve). Alternativa `ag_news`
  (~120k) via `--dataset ag_news --limit N`.
- Similaridade = 1 - distância cosseno (coleção criada com hnsw:space=cosine).
- Repo git: https://github.com/claudiomluz/semanticsearch
- Disco: ~22 GiB livres no setup; footprint estimado ~6-8 GB (torch domina).
