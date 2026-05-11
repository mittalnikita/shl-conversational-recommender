def compare_assessments(
    recommendations
):

    comparisons = []

    for item in recommendations:

        comparison = {

            "name":
                item.get("name", ""),

            "description":
                item.get(
                    "description",
                    ""
                ),

            "job_levels":
                item.get(
                    "job_levels",
                    []
                ),

            "remote_testing":
                item.get(
                    "remote_testing",
                    "unknown"
                ),

            "adaptive_support":
                item.get(
                    "adaptive_support",
                    "unknown"
                ),

            "languages":
                item.get(
                    "languages",
                    []
                ),

            "explanation":
                item.get(
                    "explanation",
                    []
                )
        }

        comparisons.append(
            comparison
        )

    return comparisons