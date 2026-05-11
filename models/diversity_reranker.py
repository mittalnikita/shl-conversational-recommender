def detect_category(name, description):

    text = (
        name + " " + description
    ).lower()

    technical_keywords = [

        "python",
        "java",
        "c++",
        "software",
        "programming",
        "developer",
        "coding"
    ]

    if any(
        keyword in text
        for keyword in technical_keywords
    ):
        return "technical"

    if (
        "leadership" in text
        or
        "manager" in text
    ):

        return "leadership"

    if (
        "personality" in text
        or
        "opq" in text
    ):

        return "personality"

    if (
        "python" in text
        or
        "java" in text
        or
        "programming" in text
    ):

        return "technical"

    if (
        "cognitive" in text
        or
        "ability" in text
        or
        "reasoning" in text
    ):

        return "cognitive"

    return "general"


def diversify_recommendations(
    recommendations,
    top_k=5
):

    diversified = []

    seen_categories = set()

    seen_signatures = set()

    for item in recommendations:

        score = item.get(
            "final_ranking_score",
            0
        )

        if score < 0.60:
            continue

        # ====================================
        # DUPLICATE SIGNATURE
        # ====================================

        signature = (
            item.get("name", "")
            .lower()
            .replace("1.0", "")
            .replace("2.0", "")
            .strip()
        )

        # Skip near duplicates

        if signature in seen_signatures:
            continue

        category = detect_category(

            item.get("name", ""),

            item.get(
                "description",
                ""
            )
        )

        name = (
            item.get(
                "name",
                ""
            )
            .lower()
        )

        # Remove weak generic assessments

        blocked_keywords = [

            "visual comparison",

            "seo",

            "statistical analysis system"
        ]

        if any(
            keyword in name
            for keyword in blocked_keywords
        ):
            continue

        # ====================================
        # CATEGORY DIVERSIFICATION
        # ====================================

        if category not in seen_categories:

            diversified.append(item)

            seen_categories.add(
                category
            )

            seen_signatures.add(
                signature
            )

        if len(diversified) >= top_k:
            break

    # ====================================
    # FILL REMAINING SLOTS
    # ====================================

    if len(diversified) < top_k:

        for item in recommendations:

            signature = (
                item.get("name", "")
                .lower()
                .replace("1.0", "")
                .replace("2.0", "")
                .strip()
            )

            if signature in seen_signatures:
                continue

            diversified.append(item)

            seen_signatures.add(
                signature
            )

            if len(diversified) >= top_k:
                break

    return diversified