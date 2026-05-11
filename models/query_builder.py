from models.query_synthesizer import (synthesize_query)
def build_search_query(
    conversation_state,
    intent=None
):
    

    requirements = (
        conversation_state.get(
            "requirements",
            []
        )
    )

    synthesize_query(requirements)

    return " ".join(
        requirements
    )