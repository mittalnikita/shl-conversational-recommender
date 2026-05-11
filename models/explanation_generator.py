def generate_explanations(
    recommendations):

    explained = []

    for item in recommendations:

        explanation_parts = []

        description = (
            item.get(
                "description",
                ""
            ).lower()
        )

        # ====================================
        # TECHNICAL
        # ====================================

        technical_keywords = [

            "python",
            "java",
            "programming",
            "software",
            "development",
            "coding"
        ]

        if any(
            keyword in description
            for keyword in technical_keywords
        ):

            explanation_parts.append(
                f"Measures skills related to "
                f"{item['name']}."
            )

        # ====================================
        # LEADERSHIP
        # ====================================

        leadership_keywords = [

            "leadership",
            "manager",
            "executive",
            "stakeholder"
        ]

        if any(
            keyword in description
            for keyword in leadership_keywords
        ):

            explanation_parts.append(
                "Includes leadership evaluation components."
            )

        # ====================================
        # PERSONALITY
        # ====================================

        personality_keywords = [

            "personality",
            "behavior",
            "opq"
        ]

        if any(
            keyword in description
            for keyword in personality_keywords
        ):

            explanation_parts.append(
                "Measures workplace personality traits."
            )

        # ====================================
        # REMOTE TESTING
        # ====================================

        if (
            item.get(
                "remote_testing",
                ""
            ).lower()
            ==
            "yes"
        ):

            explanation_parts.append(
                "Supports remote testing."
            )

        updated_item = item.copy()

        updated_item[
            "explanation"
        ] = explanation_parts

        explained.append(
            updated_item
        )

    return explained
