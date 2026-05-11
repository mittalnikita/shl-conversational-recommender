RESET_INTENTS = [
    "recommend"
]


PRESERVE_INTENTS = [
    "refine",
    "explain",
    "compare"
]


def should_reset_state(
    current_intent,
    conversation_state
):

    # ---------- Fresh Recommendation ----------

    if current_intent in RESET_INTENTS:

        return True

    # ---------- Refinement / Explanation ----------

    if current_intent in PRESERVE_INTENTS:

        return False

    return False