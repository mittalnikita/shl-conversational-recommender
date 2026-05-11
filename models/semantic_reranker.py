class SemanticReranker:

    def __init__(self):
        pass

    def rerank(
        self,
        query,
        recommendations
    ):

        for item in recommendations:

            semantic_score = item.get(
                "constraint_score",
                0
            )

            item[
                "semantic_match_score"
            ] = round(
                semantic_score,
                4
            )

            item[
                "final_ranking_score"
            ] = round(
                semantic_score,
                4
            )

        recommendations.sort(
            key=lambda x: (
                x[
                    "final_ranking_score"
                ]
            ),
            reverse=True
        )

        return recommendations