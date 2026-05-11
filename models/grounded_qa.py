def answer_catalog_question(
    user_query,
    recommendations
):

    query = user_query.lower()

    if not recommendations:

        return (
            "No recommendation context "
            "available."
        )

    top_item = recommendations[0]

    # ====================================
    # REMOTE TESTING
    # ====================================

    if (
        "remote" in query
        or
        "online" in query
    ):

        value = top_item.get(
            "remote_testing",
            "unknown"
        )

        return (
            f"{top_item['name']} "
            f"remote testing support: "
            f"{value}."
        )

    # ====================================
    # ADAPTIVE SUPPORT
    # ====================================

    if "adaptive" in query:

        value = top_item.get(
            "adaptive_support",
            "unknown"
        )

        return (
            f"{top_item['name']} "
            f"adaptive support: "
            f"{value}."
        )

    # ====================================
    # LANGUAGES
    # ====================================

    if "language" in query:

        languages = top_item.get(
            "languages",
            []
        )

        if not languages:

            return (
                f"No language information "
                f"available for "
                f"{top_item['name']}."
            )

        return (
            f"{top_item['name']} supports: "
            f"{', '.join(languages)}."
        )

    # ====================================
    # JOB LEVELS
    # ====================================

    if (
        "job level" in query
        or
        "seniority" in query
        or
        "suitable" in query
    ):

        levels = top_item.get(
            "job_levels",
            []
        )

        return (
            f"{top_item['name']} is suitable "
            f"for: {', '.join(levels)}."
        )

    # ====================================
    # DESCRIPTION
    # ====================================

    if (
        "what is" in query
        or
        "description" in query
    ):

        return (
            top_item.get(
                "description",
                "No description available."
            )
        )

    return (
        "I can answer questions about "
        "remote testing, adaptive support, "
        "languages, job levels, and "
        "assessment descriptions."
    )