import re


INTENT_EXAMPLES = {

    "recommend": [
        "recommend assessment",
        "find suitable test",
        "suggest assessments",
        "need assessment recommendation"
    ],

    "clarify": [
        "not sure",
        "need help choosing",
        "which assessment should I use",
        "ok",
        "yes",
        "continue",
        "proceed",
        "go ahead"
    ],

    "refine": [
        "add personality test",
        "include leadership evaluation",
        "remove technical assessments",
        "update recommendations"
    ],

    "explain": [
        "why was this recommended",
        "explain recommendation",
        "reason for selecting this assessment",
        "why is this suitable",
        "tell me about this assessment"
    ],

    "compare": [
        "compare these assessments",
        "difference between assessments",
        "which assessment is better",
        "compare options"
    ],

    "reject": [
        "weather today",
        "latest cricket score",
        "bitcoin price",
        "movie recommendations"
    ],

    "qa": [
        "Does this support remote testing",
        "Which languages are supported",
        "Is this adaptive",
        "What job levels are supported",
        "What does this assessment measure",
        "Is this suitable for entry-level hiring"
    ]
}


def tokenize(text):

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9 ]",
        " ",
        text
    )

    return set(text.split())


class SemanticIntentRouter:

    def __init__(self):

        self.intent_tokens = {}

        self._build_intent_index()

    def _build_intent_index(self):

        for intent, examples in (
            INTENT_EXAMPLES.items()
        ):

            token_set = set()

            for example in examples:

                tokens = tokenize(example)

                token_set.update(tokens)

            self.intent_tokens[
                intent
            ] = token_set

    def compute_similarity(
        self,
        query_tokens,
        intent_tokens
    ):

        intersection = len(
            query_tokens.intersection(
                intent_tokens
            )
        )

        union = len(
            query_tokens.union(
                intent_tokens
            )
        )

        if union == 0:
            return 0.0

        return intersection / union

    def detect_intent(
        self,
        query
    ):

        query_tokens = tokenize(query)

        best_intent = "recommend"

        best_score = 0.0

        for intent, intent_tokens in (
            self.intent_tokens.items()
        ):

            score = self.compute_similarity(
                query_tokens,
                intent_tokens
            )

            if score > best_score:

                best_score = score

                best_intent = intent

        # fallback heuristics

        query_lower = query.lower()

        if any(
            word in query_lower
            for word in [
                "compare",
                "difference",
                "better"
            ]
        ):

            best_intent = "compare"

        elif any(
            word in query_lower
            for word in [
                "explain",
                "why",
                "tell me about"
            ]
        ):

            best_intent = "explain"

        elif any(
            word in query_lower
            for word in [
                "also",
                "include",
                "add",
                "remove"
            ]
        ):

            best_intent = "refine"

        return {
            "intent": best_intent,
            "score": round(
                best_score,
                4
            )
        }


def main():

    router = SemanticIntentRouter()

    while True:

        query = input("\nQuery: ")

        if query.lower() == "exit":
            break

        result = router.detect_intent(
            query
        )

        print("\nIntent Result:\n")

        print(result)


if __name__ == "__main__":
    main()