# STATUS — Semantic Search POC

> Última atualização: 2026-07-13

## Objetivo
POC de aprendizado sobre busca semântica com banco vetorial e RAG, indexando
artigos jornalísticos em inglês, com interface para busca estruturada ou chat.

## Fase atual
em desenvolvimento

## Feito recentemente
- [2026-07-13] Página de ajuda (`src/static/help.html`) com diagrama de
  arquitetura em SVG (theme-aware), linkada do app via botão "📖 Ajuda".
  Static serving do Streamlit habilitado em `.streamlit/config.toml`.
- [2026-07-12] Scaffold completo, deps instaladas, dataset bbc-news indexado
  (3594 chunks / 1225 artigos), busca e RAG validados ponta a ponta.
- [2026-07-12] Commit inicial + push para o GitHub.

## Em andamento
- Nada aberto.

## Próximos passos
1. Expandir a página de ajuda (reindexação, troca de modelo, ajuste de top-K).
2. Experimento: trocar embedding para `all-mpnet-base-v2` e comparar scores.
3. Opcional: testar dataset `ag_news` (120k) para ver escala.

## Bloqueios / decisões pendentes
- Nenhum. (torch precisa ter wheel para Python 3.13 — validar no pip install.)

## Notas de contexto
- Embedding: all-MiniLM-L6-v2 (384 dims, inglês). Banco: ChromaDB persistente
  em `data/chroma/` (git-ignored). LLM RAG: qwen2.5:3b via Ollama
  (trocado do llama3.2:1b em 2026-07-13 por melhor qualidade em PT).
- Dataset padrão: `SetFit/bbc-news` (~2k artigos, leve). Alternativa `ag_news`
  (~120k) via `--dataset ag_news --limit N`.
- Similaridade = 1 - distância cosseno (coleção criada com hnsw:space=cosine).
- Repo git: https://github.com/claudiomluz/semanticsearch
- Disco: ~22 GiB livres no setup; footprint estimado ~6-8 GB (torch domina).
