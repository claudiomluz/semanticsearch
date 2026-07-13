# STATUS — Semantic Search POC

> Última atualização: 2026-07-13

## Objetivo
POC de aprendizado sobre busca semântica com banco vetorial e RAG, indexando
artigos jornalísticos em inglês, com interface para busca estruturada ou chat.

## Fase atual
em desenvolvimento

## Feito recentemente
- [2026-07-13] FAQ da ajuda completo, cobrindo as 8 caixas do diagrama,
  em duas seções: Indexação (Dataset, Chunking, Embedding, ChromaDB) e
  Consulta (Resultado estruturado, Monta prompt, LLM local, Resposta +
  fontes). Diagramas SVG para chunking e ChromaDB. Texto conceitual, sem
  citar código.
- [2026-07-13] Interface e página de ajuda bilíngues (PT/EN) com seletor
  de idioma; RAG responde no idioma escolhido. Módulo `src/i18n.py`.
- [2026-07-13] Troca do LLM: llama3.2:1b -> qwen2.5:3b (melhor PT); llama
  removido, mantido só 1 modelo.
- [2026-07-13] Página de ajuda (`src/static/help.html`) com diagrama de
  arquitetura em SVG (theme-aware), linkada do app via botão "📖 Ajuda".
  Static serving do Streamlit habilitado em `.streamlit/config.toml`.
- [2026-07-12] Scaffold completo, deps instaladas, dataset bbc-news indexado
  (3594 chunks / 1225 artigos), busca e RAG validados ponta a ponta.
- [2026-07-12] Commit inicial + push para o GitHub.

## Em andamento
- Nada aberto.

## Próximos passos
1. Experimento: trocar embedding para `all-mpnet-base-v2` e comparar scores.
2. Opcional: testar dataset `ag_news` (120k) para ver escala.
3. Possíveis novos tópicos de ajuda: reindexação e ajuste de top-K.

## Bloqueios / decisões pendentes
- Nenhum.

## Notas de contexto
- Embedding: all-MiniLM-L6-v2 (384 dims, inglês). Banco: ChromaDB persistente
  em `data/chroma/` (git-ignored). LLM RAG: qwen2.5:3b via Ollama
  (trocado do llama3.2:1b em 2026-07-13 por melhor qualidade em PT).
- Dataset padrão: `SetFit/bbc-news` (~2k artigos, leve). Alternativa `ag_news`
  (~120k) via `--dataset ag_news --limit N`.
- Similaridade = 1 - distância cosseno (coleção criada com hnsw:space=cosine).
- Interface bilíngue PT/EN via `src/i18n.py` (seletor no topo do app).
- Ajuda em `src/static/help.html` (servida em /app/static/), bilíngue com
  alternância por CSS (data-lang) + ?lang= na URL. FAQ conceitual, evita
  citar classes/funções/arquivos do projeto (preferência do usuário).
- Repo git: https://github.com/claudiomluz/semanticsearch
- Disco: ~22 GiB livres no setup; footprint estimado ~6-8 GB (torch domina).
