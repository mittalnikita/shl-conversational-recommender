import numpy as np

from sentence_transformers import (
    SentenceTransformer
)


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


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
        "why is this suitable"
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
        "Does this support remote testing?",
        "Which languages are supported?",
        "Is this adaptive?",
        "What job levels are supported?",
        "What does this assessment measure?",
        "Is this suitable for entry-level hiring?"
    ]
}


class SemanticIntentRouter:

    def __init__(self):

        self.model = SentenceTransformer(
            MODEL_NAME
        )

        self.intent_embeddings = {}

        self._build_intent_index()

    def _build_intent_index(self):

        for intent, examples in (
            INTENT_EXAMPLES.items()
        ):

            embeddings = self.model.encode(
                examples,
                normalize_embeddings=True
            )

            centroid = np.mean(
                embeddings,
                axis=0
            )

            self.intent_embeddings[
                intent
            ] = centroid

    def detect_intent(self, query):

        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        best_intent = None
        best_score = -1

        for intent, centroid in (
            self.intent_embeddings.items()
        ):

            score = np.dot(
                query_embedding,
                centroid
            )

            if score > best_score:

                best_score = score
                best_intent = intent

        return {
            "intent": best_intent,
            "score": float(best_score)
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