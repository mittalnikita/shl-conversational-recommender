from sentence_transformers import (
    CrossEncoder
)

import numpy as np


MODEL_NAME = (
    "cross-encoder/ms-marco-MiniLM-L-2-v2"
)


class SemanticReranker:

    def __init__(self):

        self.model = CrossEncoder(
            MODEL_NAME
        )

    def rerank(
        self,
        query,
        recommendations
    ):

        if not recommendations:
            return []

        pairs = []

        for item in recommendations:

            text = (

                item["name"]

                +

                " "

                +

                item.get(
                    "description",
                    ""
                )

            )

            pairs.append(
                [query, text]
            )

        raw_scores = (
            self.model.predict(
                pairs
            )
        )

        # ====================================
        # NORMALIZE SCORES
        # ====================================

        min_score = np.min(raw_scores)

        max_score = np.max(raw_scores)

        normalized_scores = []

        for score in raw_scores:

            if max_score > min_score:

                normalized = (
                    (score - min_score)
                    /
                    (max_score - min_score)
                )

            else:

                normalized = 0.5

            normalized_scores.append(
                float(normalized)
            )

        reranked = []

        for item, score in zip(
            recommendations,
            normalized_scores
        ):

            updated_item = item.copy()

            updated_item[
                "semantic_match_score"
            ] = round(score, 4)

            # ====================================
            # FINAL FUSION SCORE
            # ====================================

            updated_item[
                "final_ranking_score"
            ] = round(

                (
                    0.7 * item.get(
                        "reranked_score",
                        0
                    )
                    +
                    0.3 * score
                ),

                4
            )

            reranked.append(
                updated_item
            )

        reranked.sort(

            key=lambda x: (
                x[
                    "final_ranking_score"
                ]
            ),

            reverse=True
        )

        return reranked