from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from models.recommendation_pipeline import (
    initialize_system,
    recommend
)
from models.conversation_reconstructor import (
    reconstruct_conversation_state
)
from models.intent_router import (
    SemanticIntentRouter
)

# =====================================
# FASTAPI APP
# =====================================

app = FastAPI()

# =====================================
# LOAD SYSTEM ONCE
# =====================================

system = initialize_system()

intent_router = (
    SemanticIntentRouter()
)

# =====================================
# REQUEST SCHEMA
# =====================================

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]

# =====================================
# HEALTH ENDPOINT
# =====================================

@app.get("/health")
def health_check():

    return {
        "status": "ok"
    }


# =====================================
# CHAT ENDPOINT
# =====================================

@app.post("/chat")
def chat(request: ChatRequest):

    messages = [

        {
            "role": msg.role,
            "content": msg.content
        }

        for msg in request.messages
    ]

    # ---------------------------------
    # RECONSTRUCT STATE
    # ---------------------------------

    reconstruction = (
        reconstruct_conversation_state(
            messages,
            intent_router.detect_intent
        )
    )

    conversation_state = (
        reconstruction[
            "conversation_state"
        ]
    )

    latest_query = (
        reconstruction[
            "latest_query"
        ]
    )

    # ---------------------------------
    # RUN RECOMMENDATION PIPELINE
    # ---------------------------------

    result = recommend(

        user_query=latest_query,

        conversation_state=
            conversation_state,

        catalog=system["catalog"],

        bm25=system["bm25"],

        index=system["index"],

        model=system["model"],

        policy_engine=
            system["policy_engine"],

        semantic_reranker=
            system[
                "semantic_reranker"
            ],

        response_generator=system["response_generator"],
        
        domain_classifier= system["domain_classifier"]
    )

    if ("conversation_state" in result):

        clean_state = {
            k: v
            for k, v in (
                result[
                    "conversation_state"
                ].items()
            )

            if k != "last_recommendations"
        }

        result[
            "conversation_state"
        ] = clean_state

    return result