import json
import faiss
from pathlib import Path
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from models.dialog_policy import (DialogPolicyEngine)
from models.conversation_state import ( initialize_state)
from models.semantic_reranker import (SemanticReranker)
from models.explanation_generator import (generate_explanations)
from models.query_builder import (build_search_query)
from models.grounded_qa import (answer_catalog_question)
from models.response_generator import (ResponseGenerator)
from models.diversity_reranker import (diversify_recommendations)
from models.compare_assessment import (compare_assessments)
from models.explain_assessment import (explain_assessment)
from models.domain_classifier import (DomainClassifier)

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

CATALOG_FILE = DATA_DIR / "catalog.json"

FAISS_INDEX_FILE = (DATA_DIR / "shl_index.faiss")

# ---------- FAISS ----------

import os
import faiss
import numpy as np


def build_faiss_index(
    catalog,
    model
):

    texts = []

    for item in catalog:

        text = (
            item.get("name", "")
            + " "
            + item.get(
                "description",
                ""
            )
        )

        texts.append(text)

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings.astype(
            np.float32
        )
    )

    return index


def load_faiss_index(
    catalog,
    model
):

    if os.path.exists(
        FAISS_INDEX_FILE
    ):

        return faiss.read_index(
            str(FAISS_INDEX_FILE)
        )

    print(
        "Building FAISS index..."
    )

    index = build_faiss_index(
        catalog,
        model
    )

    faiss.write_index(
        index,
        str(FAISS_INDEX_FILE)
    )

    return index


def initialize_system():

    print("Loading system...")
    catalog = load_catalog()
    bm25 = build_bm25(catalog)
    index = load_faiss_index(catalog, model)
    model = load_model()

    policy_engine = (
        DialogPolicyEngine()
    )

    domain_classifier = (
        DomainClassifier()
    )

    semantic_reranker = (
        SemanticReranker()
    )

    response_generator = (
        ResponseGenerator()
    )

    return {
        "catalog": catalog,
        "bm25": bm25,
        "index": index,
        "model": model,
        "policy_engine": policy_engine,
        "semantic_reranker": semantic_reranker,
        "response_generator": response_generator,
        "domain_classifier": domain_classifier
    }

# ---------- Load Catalog ----------

def load_catalog():

    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- Tokenization ----------

def tokenize(text):
    return text.lower().split()


# ---------- BM25 ----------

def build_bm25(catalog):

    corpus = [
        tokenize(item["search_text"])
        for item in catalog
    ]

    return BM25Okapi(corpus)


# ---------- FAISS ----------

def load_faiss():
    return faiss.read_index(str(FAISS_INDEX_FILE))


# ---------- Embedding Model ----------

def load_model():
    return SentenceTransformer(MODEL_NAME)

# ---------- Hybrid Search ----------

def hybrid_search(
    query,
    catalog,
    bm25,
    index,
    model,
    top_k=5
):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    semantic_scores, semantic_indices = index.search(
        query_embedding,
        len(catalog)
    )

    semantic_scores = semantic_scores[0]
    semantic_indices = semantic_indices[0]

    # Normalize semantic scores

    semantic_min = np.min(semantic_scores)
    semantic_max = np.max(semantic_scores)

    if semantic_max > semantic_min:
        semantic_scores = (
            (semantic_scores - semantic_min)
            /
            (semantic_max - semantic_min)
        )

    semantic_dict = {}

    for idx, score in zip(
        semantic_indices,
        semantic_scores
    ):
        semantic_dict[idx] = float(score)

    # BM25

    bm25_scores = bm25.get_scores(
        tokenize(query)
    )

    # Normalize BM25

    bm25_min = np.min(bm25_scores)
    bm25_max = np.max(bm25_scores)

    if bm25_max > bm25_min:
        bm25_scores = (
            (bm25_scores - bm25_min)
            /
            (bm25_max - bm25_min)
        )

    # Final scoring

    results = []

    for idx, item in enumerate(catalog):

        semantic_score = semantic_dict.get(idx, 0)

        keyword_score = bm25_scores[idx]

        final_score = (
            0.45 * semantic_score
            +
            0.55 * keyword_score
        )

        results.append({

            "name": item["name"],

            "url": item["url"],

            "description": item.get(
                "description",
                ""
            ),

            "job_levels": item.get(
                "job_levels",
                []
            ),

            "remote_testing": item.get(
                "remote_testing",
                ""
            ),

            "adaptive_support": item.get(
                "adaptive_support",
                ""
            ),

            "languages": item.get(
                "languages",
                []
            ),

            "final_score": final_score
        })

    results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return results[:15]


# ---------- Recommendation Pipeline ----------

def recommend(
    user_query,
    conversation_state,
    catalog,
    bm25,
    index,
    model,
    policy_engine,
    semantic_reranker,
    response_generator,
    domain_classifier
):
    
    domain_result = (
        domain_classifier.classify(
            user_query
        )
    )

    if (
        domain_result["domain"]
        ==
        "out_of_scope"
    ):

        return {

            "status": "rejected",

            "policy": {

                "message":
                (
                    "I can only assist with "
                    "SHL assessment recommendations "
                    "and catalog-grounded queries."
                )
            }
        }

    intent_result = (
        policy_engine.intent_router.detect_intent(
            user_query
        )
    )

    intent = intent_result["intent"]

    policy_result = (
        policy_engine.evaluate(
            user_query,
            conversation_state
        )
    )

    if policy_result["intent"] == "qa":

        answer = (
            answer_catalog_question(
                user_query,
                conversation_state.get("last_recommendations",[])))
        
        return {
            "status": "qa_response",
            "response": answer,
            "policy": policy_result
        }

    if policy_result["action"] == "clarify":

        return {
            "status": "clarification_needed",
            "policy": policy_result,
            "conversation_state": (conversation_state)
        }

    if policy_result["action"] == "reject":

        return {
            "status": "rejected",
            "policy": policy_result
        }

    # ====================================
    # EXPLAIN FLOW
    # ====================================

    if policy_result["action"] == "explain":

        target_assessment = (
            explain_assessment(
                user_query,
                conversation_state.get(
                    "last_recommendations",
                    []
                )
            )
        )

        if not target_assessment:

            return {
                "status": "explanation_error",
                "message": (
                    "Could not identify which "
                    "assessment you want explained."
                )
            }

        explanation_prompt = f"""
        Explain this SHL assessment naturally.

        Assessment Name:
        {target_assessment['name']}

        Description:
        {target_assessment['description']}

        Job Levels:
        {target_assessment['job_levels']}

        Remote Testing:
        {target_assessment['remote_testing']}

        Adaptive Support:
        {target_assessment['adaptive_support']}

        Explain:
        - what it evaluates
        - when recruiters use it
        - which candidate types it suits best
        - important capabilities measured

        Keep answer concise and grounded.
        """

        natural_explanation = (
            response_generator.generate_text(
                explanation_prompt
            )
        )

        return {
            "status": "explanation",
            "response": natural_explanation
        }

    search_query = (
        build_search_query(
            conversation_state,
            policy_result["intent"]
        )
    )

    results = hybrid_search(
        query=search_query,
        catalog=catalog,
        bm25=bm25,
        index=index,
        model=model
    )

    final_results = (
        semantic_reranker.rerank(
            search_query,
            results
        )
    )
    diversified_results = (
        diversify_recommendations(
            final_results
        )
    )
    explained_results = (
        generate_explanations(
            diversified_results)
    )
    if policy_result["action"] == "compare":

        comparison_data = (
            compare_assessments(
                explained_results
            )
        )

        comparison_response = (
            response_generator
            .generate_comparison_response(
                user_query,
                comparison_data
            )
        )

        return {

            "status": "comparison",

            "comparison_data":
                comparison_data,

            "response":
                comparison_response,

            "conversation_state":
                conversation_state,

            "policy":
                policy_result
        }
    
    natural_response = (
        response_generator
        .generate_recommendation_response(
            user_query,
            explained_results
        )
    )
    conversation_state["last_recommendations"] = explained_results

    return {
        "status": "success",
        "search_query": search_query,
        "recommendations": explained_results,
        "conversation_state": conversation_state,
        "policy": policy_result,
        "response": natural_response,
    }

# ---------- Main ----------

def main():

    print("Loading system...")

    catalog = load_catalog()
    bm25 = build_bm25(catalog)
    index = load_faiss()
    model = load_model()
    policy_engine = DialogPolicyEngine()
    semantic_reranker = (SemanticReranker())
    response_generator = (ResponseGenerator())
    conversation_state = initialize_state()

    while True:

        query = input("\nUser Query: ")

        if query.lower() == "exit":
            break

        result = recommend(
            query,
            conversation_state,
            catalog,
            bm25,
            index,
            model,
            policy_engine,
            semantic_reranker,
            response_generator
        )

        print("\nSYSTEM OUTPUT:\n")

        print(
            json.dumps(
                result,
                indent=4
            )
        )


if __name__ == "__main__":
    main()