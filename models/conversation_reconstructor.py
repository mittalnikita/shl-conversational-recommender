from models.conversation_state import (
    initialize_state,
    merge_state
)


def reconstruct_conversation_state(
    messages,
    intent_router
):

    state = initialize_state()

    latest_query = ""

    latest_intent = "recommend"

    for message in messages:

        if (
            message["role"]
            != "user"
        ):
            continue

        user_query = (
            message["content"]
        )

        latest_query = user_query

        state = merge_state(
            state,
            user_query
        )

        intent_result = (
            intent_router(user_query)
        )

        latest_intent = (
            intent_result["intent"]
        )

    return {

        "conversation_state":
            state,

        "latest_query":
            latest_query,

        "latest_intent":
            latest_intent
    }