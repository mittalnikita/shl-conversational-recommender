def explain_assessment(
    user_query,
    recommendations
):

    query = user_query.lower()

    for item in recommendations:

        name = item.get(
            "name",
            ""
        ).lower()

        if name in query:

            return item

    return None