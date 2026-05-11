import numpy as np

from sentence_transformers import (
    SentenceTransformer
)


MODEL_NAME = (
    "BAAI/bge-small-en-v1.5"
)


IN_DOMAIN_EXAMPLES = [

    "recommend assessment for python developer",
    "leadership assessment for managers",
    "compare SHL assessments",
    "technical hiring assessment",
    "personality test for hiring",
    "which assessment supports remote testing",
    "assessment recommendation for data scientist",
    "cognitive ability assessment"
]


OUT_OF_DOMAIN_EXAMPLES = [

    "weather today",
    "latest cricket score",
    "bitcoin price",
    "railway jobs",
    "group d jobs",
    "movie recommendations",
    "best restaurants nearby",
    "UPSC preparation",
    "government exam updates"
]


class DomainClassifier:

    def __init__(self):

        self.model = SentenceTransformer(
            MODEL_NAME
        )

        self.in_domain_embedding = (
            self._build_centroid(
                IN_DOMAIN_EXAMPLES
            )
        )

        self.out_domain_embedding = (
            self._build_centroid(
                OUT_OF_DOMAIN_EXAMPLES
            )
        )

    def _build_centroid(
        self,
        examples
    ):

        embeddings = self.model.encode(
            examples,
            normalize_embeddings=True
        )

        return np.mean(
            embeddings,
            axis=0
        )

    def classify(
        self,
        query
    ):

        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        in_score = np.dot(
            query_embedding,
            self.in_domain_embedding
        )

        out_score = np.dot(
            query_embedding,
            self.out_domain_embedding
        )

        if out_score > in_score:

            return {
                "domain": "out_of_scope",
                "confidence":
                    float(out_score)
            }

        return {
            "domain": "shl_assessment",
            "confidence":
                float(in_score)
        }