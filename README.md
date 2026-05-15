# SHL Conversational Assessment Recommendation System

AI-powered conversational recommendation engine for SHL assessments using conversational AI, retrieval orchestration, recruiter-style responses, conversational refinement, and grounded explainability.

---

## Live Demo

🚀 Deployed Application:  
https://nikitamittal123-shl-conversational-recommender.hf.space/

---

## Key Features

- Conversational SHL assessment recommendation
- Conversational refinement and follow-up queries
- Assessment comparison workflows
- Grounded explainability generation
- Conversational memory reconstruction
- Clarification handling
- Out-of-scope query rejection
- Recruiter-style natural responses
- Streamlit frontend + FastAPI backend

---

## Example Queries

```text
Need Python developer assessment
```

```text
Also include leadership evaluation
```

```text
Compare the first two assessments
```

```text
Explain why this assessment was recommended
```

---

## System Architecture

```mermaid
flowchart TD

A[User Query]
--> B[Conversation Reconstruction]

B --> C[Intent Detection]

C --> D[Constraint Extraction]

D --> E[Query Synthesis]

E --> F[Hybrid Retrieval]

F --> G[Reranking]

G --> H[Explanation Generation]

H --> I[LLM Response Generation]

I --> J[Frontend Response]
```

---

## Tech Stack

<p align="left">

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="45" height="45"/>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="45" height="45"/>
<img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" width="120"/>
<img src="https://avatars.githubusercontent.com/u/78043063?s=200&v=4" width="45" height="45"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" width="70"/>
<img src="https://numpy.org/images/logo.svg" width="70"/>
<img src="https://pandas.pydata.org/static/img/pandas_mark.svg" width="45" height="45"/>
<img src="https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/dark/groq.png" width="45" height="45"/>

</p>

| Layer | Technologies |
|---|---|
| Backend | FastAPI, Python |
| Frontend | Streamlit |
| Conversational AI | Intent Routing, Dialog Policy Engine, Query Synthesis |
| Retrieval | BM25, Retrieval Orchestration |
| NLP Pipeline | Constraint Extraction, Conversation Reconstruction |
| LLM Integration | Groq API, Llama 3.1 8B Instant |
| Data Processing | NumPy, Pandas, Scikit-learn |
| Deployment | Hugging Face Spaces |

---

## Repository Structure

```text
SHL/
├── api/
├── data/
├── frontend/
├── models/
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Core Capabilities

| Capability | Description |
|---|---|
| Recommendation | Recommends SHL assessments conversationally |
| Refinement | Supports iterative recommendation refinement |
| Explainability | Explains recommendation reasoning |
| Comparison | Compares assessments conversationally |
| QA | Answers catalog-grounded questions |
| Rejection | Rejects unrelated/out-of-scope queries |

---

## Deployment

Frontend Deployment:  
https://nikitamittal123-shl-conversational-recommender.hf.space/

GitHub Repository:  
https://github.com/mittalnikita/shl-conversational-recommender

---

## Future Improvements

- Ontology-based normalization
- Stronger semantic reranking
- Multilingual support
- Recruiter analytics dashboard
- Advanced conversational planning

---

## Conclusion

This project demonstrates a modular conversational AI system for SHL assessment recommendation using conversational orchestration, retrieval engineering, grounded explainability, and recruiter-style interaction workflows.
