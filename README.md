# SHL Conversational Assessment Recommender

Conversational AI system for recommending SHL assessments using:
- FastAPI
- FAISS
- BM25
- Sentence Transformers
- Cross Encoder Reranking
- Streamlit frontend

## Features
- Conversational recommendations
- Clarification handling
- Refinement support
- Assessment comparison
- Out-of-scope refusal
- Stateless conversation reconstruction

## Run Backend

```bash
uvicorn api.main:app --reload

## Run Frontend

```bash
streamlit run frontend/app.py