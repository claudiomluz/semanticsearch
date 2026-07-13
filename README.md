# Semantic Search POC

Projeto experimental de aprendizado sobre **busca semântica com banco vetorial**
e **RAG**, usando artigos jornalísticos em inglês.

Dois caminhos de interação:
- **Busca (estruturada):** query retorna lista de artigos com título, categoria e
  score de similaridade.
- **Chat (conversacional):** RAG — recupera trechos relevantes e um LLM local
  responde em linguagem natural, citando as fontes.

## Stack

| Camada | Tecnologia |
|---|---|
| Embedding | `all-MiniLM-L6-v2` (sentence-transformers), local, 384 dims |
| Banco vetorial | ChromaDB (persistente em disco) |
| LLM (RAG) | `qwen2.5:3b` via [Ollama](https://ollama.com) |
| Interface | Streamlit |
| Dados | `SetFit/bbc-news` ou `ag_news` (HuggingFace datasets) |

## Pré-requisitos

- Python 3.13 (venv já criado em `venv/`)
- [Ollama](https://ollama.com) instalado e rodando

## Setup

```bash
# 1. Instalar dependências (dentro do venv)
./venv/bin/pip install -r requirements.txt

# 2. Baixar o LLM local
ollama pull qwen2.5:3b

# 3. Indexar os artigos no ChromaDB (bbc: ~2k artigos, leve)
./venv/bin/python src/ingest.py
#   ou dataset maior:  ./venv/bin/python src/ingest.py --dataset ag_news --limit 5000

# 4. Rodar a interface
./venv/bin/streamlit run src/app.py
```

## Testes rápidos por linha de comando

```bash
./venv/bin/python src/search.py "technology company earnings"
./venv/bin/python src/rag.py "What happened in the technology sector?"
```

## Estrutura

```
src/
  config.py   # parâmetros centrais (modelo, dataset, top-k, caminhos)
  db.py       # ChromaDB + modelo de embedding (carregados 1x)
  ingest.py   # baixa dataset, chunk, embedding, popula o Chroma
  search.py   # busca semântica pura
  rag.py      # retrieval + LLM (Ollama)
  app.py      # interface Streamlit
data/chroma/  # persistência do banco vetorial (git-ignored)
```

## Conceitos exercitados

- **Embedding:** texto → vetor que captura significado.
- **Busca vetorial (ANN):** achar vizinhos mais próximos por similaridade de cosseno.
- **Chunking:** quebrar artigos longos em pedaços para indexação precisa.
- **RAG:** injetar trechos recuperados no prompt do LLM para respostas ancoradas
  em fontes reais, reduzindo alucinação.
