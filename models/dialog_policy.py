from models.intent_router import (
    SemanticIntentRouter
)


class DialogPolicyEngine:

    def __init__(self):

        self.intent_router = (
            SemanticIntentRouter()
        )

    def evaluate(
        self,
        user_query,
        conversation_state
    ):

        intent_result = (
            self.intent_router.detect_intent(
                user_query
            )
        )

        intent = (
            intent_result["intent"]
        )

        # ====================================
        # SEMANTIC CONTEXT
        # ====================================

        requirements = (
            conversation_state.get(
                "requirements",
                []
            )
        )

        combined_text = " ".join(
            requirements
        ).strip().lower()

        # ====================================
        # CLARIFICATION
        # ====================================

        if len(combined_text.split()) < 4:

            return {

                "action": "clarify",

                "intent": "clarify",

                "reason":
                    "insufficient_context",

                "message":
                    (
                        "Could you describe the "
                        "role, required skills, "
                        "or assessment needs in "
                        "more detail?"
                    )
            }

        # ====================================
        # REJECT
        # ====================================

        if intent == "reject":

            return {

                "action": "reject",

                "intent": intent,

                "reason":
                    "out_of_scope",

                "message":
                    (
                        "I can only assist with "
                        "SHL assessment recommendations "
                        "and catalog-grounded queries."
                    )
            }

        # ====================================
        # EXPLAIN
        # ====================================

        if intent == "explain":

            return {

                "action": "explain",

                "intent": intent,

                "reason":
                    "user_requested_explanation",

                "message":
                    (
                        "Generating explanation."
                    )
            }

        # ====================================
        # COMPARE
        # ====================================

        if intent == "compare":

            return {

                "action": "compare",

                "intent": intent,

                "reason":
                    "user_requested_comparison",

                "message":
                    (
                        "Comparing assessments."
                    )
            }

        # ====================================
        # REFINE
        # ====================================

        if intent == "refine":

            return {

                "action": "refine",

                "intent": intent,

                "reason":
                    "user_requested_refinement",

                "message":
                    (
                        "Refining recommendations."
                    )
            }

        # ====================================
        # DEFAULT RECOMMEND
        # ====================================

        return {

            "action": "recommend",

            "intent": "recommend",

            "reason":
                "sufficient_information",

            "message":
                (
                    "Generating recommendations."
                )
        }
