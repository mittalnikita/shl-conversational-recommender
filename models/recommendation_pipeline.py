import json
from pathlib import Path

from rank_bm25 import BM25Okapi

from models.dialog_policy import (
    DialogPolicyEngine
)

from models.conversation_state import (
    initialize_state
)

from models.semantic_reranker import (
    SemanticReranker
)

from models.explanation_generator import (
    generate_explanations
)

from models.query_builder import (
    build_search_query
)

from models.grounded_qa import (
    answer_catalog_question
)

from models.response_generator import (
    ResponseGenerator
)

from models.diversity_reranker import (
    diversify_recommendations
)

from models.compare_assessment import (
    compare_assessments
)

from models.explain_assessment import (
    explain_assessment
)

from models.domain_classifier import (
    DomainClassifier
)

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

CATALOG_FILE = (
    DATA_DIR / "catalog.json"
)

# ====================================
# LOAD CATALOG
# ====================================

def load_catalog():

    with open(
        CATALOG_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ====================================
# TOKENIZATION
# ====================================

def tokenize(text):

    return text.lower().split()


# ====================================
# BM25
# ====================================

def build_bm25(catalog):

    corpus = [

        tokenize(
            item["search_text"]
        )

        for item in catalog
    ]

    return BM25Okapi(corpus)


# ====================================
# SYSTEM INIT
# ====================================

def initialize_system():

    print("Loading system...")

    catalog = load_catalog()

    bm25 = build_bm25(
        catalog
    )

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

        "policy_engine":
            policy_engine,

        "semantic_reranker":
            semantic_reranker,

        "response_generator":
            response_generator,

        "domain_classifier":
            domain_classifier
    }


# ====================================
# LIGHTWEIGHT HYBRID SEARCH
# ====================================

def hybrid_search(
    query,
    catalog,
    bm25,
    top_k=15
):

    bm25_scores = bm25.get_scores(
        tokenize(query)
    )

    results = []

    for idx, item in enumerate(
        catalog
    ):

        keyword_score = float(
            bm25_scores[idx]
        )

        results.append({

            "name":
                item["name"],

            "url":
                item["url"],

            "description":
                item.get(
                    "description",
                    ""
                ),

            "job_levels":
                item.get(
                    "job_levels",
                    []
                ),

            "remote_testing":
                item.get(
                    "remote_testing",
                    ""
                ),

            "adaptive_support":
                item.get(
                    "adaptive_support",
                    ""
                ),

            "languages":
                item.get(
                    "languages",
                    []
                ),

            "final_score":
                keyword_score
        })

    results.sort(
        key=lambda x: (
            x["final_score"]
        ),
        reverse=True
    )

    return results[:top_k]


# ====================================
# MAIN RECOMMENDATION PIPELINE
# ====================================

def recommend(

    user_query,

    conversation_state,

    catalog,

    bm25,

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

    # ====================================
    # OUT OF SCOPE
    # ====================================

    if (
        domain_result["domain"]
        ==
        "out_of_scope"
    ):

        return {

            "status":
                "rejected",

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
        policy_engine
        .intent_router
        .detect_intent(
            user_query
        )
    )

    policy_result = (
        policy_engine.evaluate(
            user_query,
            conversation_state
        )
    )

    # ====================================
    # QA
    # ====================================

    if (
        policy_result["intent"]
        ==
        "qa"
    ):

        answer = (
            answer_catalog_question(

                user_query,

                conversation_state.get(
                    "last_recommendations",
                    []
                )
            )
        )

        return {

            "status":
                "qa_response",

            "response":
                answer,

            "policy":
                policy_result
        }

    # ====================================
    # CLARIFICATION
    # ====================================

    if (
        policy_result["action"]
        ==
        "clarify"
    ):

        return {

            "status":
                "clarification_needed",

            "policy":
                policy_result,

            "conversation_state":
                conversation_state
        }

    # ====================================
    # REJECT
    # ====================================

    if (
        policy_result["action"]
        ==
        "reject"
    ):

        return {

            "status":
                "rejected",

            "policy":
                policy_result
        }

    # ====================================
    # EXPLAIN FLOW
    # ====================================

    if (
        policy_result["action"]
        ==
        "explain"
    ):

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

                "status":
                    "explanation_error",

                "message":
                    (
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

            "status":
                "explanation",

            "response":
                natural_explanation
        }

    # ====================================
    # SEARCH QUERY
    # ====================================

    search_query = (
        build_search_query(
            conversation_state,
            policy_result["intent"]
        )
    )

    # ====================================
    # RETRIEVAL
    # ====================================

    results = hybrid_search(

        query=search_query,

        catalog=catalog,

        bm25=bm25
    )

    # ====================================
    # RERANK
    # ====================================

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
            diversified_results
        )
    )

    # ====================================
    # COMPARE FLOW
    # ====================================

    if (
        policy_result["action"]
        ==
        "compare"
    ):

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

            "status":
                "comparison",

            "comparison_data":
                comparison_data,

            "response":
                comparison_response,

            "conversation_state":
                conversation_state,

            "policy":
                policy_result
        }

    # ====================================
    # NATURAL RESPONSE
    # ====================================

    natural_response = (

        response_generator
        .generate_recommendation_response(

            user_query,

            explained_results
        )
    )

    conversation_state[
        "last_recommendations"
    ] = explained_results

    return {

        "status":
            "success",

        "search_query":
            search_query,

        "recommendations":
            explained_results,

        "conversation_state":
            conversation_state,

        "policy":
            policy_result,

        "response":
            natural_response,
    }


# ====================================
# MAIN
# ====================================

def main():

    print("Loading system...")

    system = initialize_system()

    conversation_state = (
        initialize_state()
    )

    while True:

        query = input(
            "\nUser Query: "
        )

        if query.lower() == "exit":
            break

        result = recommend(

            user_query=query,

            conversation_state=
                conversation_state,

            catalog=
                system["catalog"],

            bm25=
                system["bm25"],

            policy_engine=
                system["policy_engine"],

            semantic_reranker=
                system[
                    "semantic_reranker"
                ],

            response_generator=
                system[
                    "response_generator"
                ],

            domain_classifier=
                system[
                    "domain_classifier"
                ]
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