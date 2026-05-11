STOPWORDS = {

    "need",
    "want",
    "assessment",
    "assessments",
    "for",
    "with",
    "mainly",
    "required",
    "requirement",
    "looking"
}

# =====================================
# SEMANTIC NORMALIZATION MAP
# =====================================

NORMALIZATION_MAP = {

    # ---------------------------------
    # SOFTWARE / PROGRAMMING
    # ---------------------------------

    "software developer":
        [
            "software engineering",
            "programming",
            "coding"
        ],

    "software engineer":
        [
            "software engineering",
            "programming"
        ],

    "programmer":
        [
            "programming",
            "coding"
        ],

    # ---------------------------------
    # LANGUAGES
    # ---------------------------------

    "python":
        [
            "python programming"
        ],

    "java":
        [
            "java programming"
        ],

    "c++":
        [
            "c++ programming"
        ],

    "javascript":
        [
            "javascript programming"
        ],

    # ---------------------------------
    # COGNITIVE / ANALYTICAL
    # ---------------------------------

    "problem solving":
        [
            "analytical reasoning",
            "cognitive ability"
        ],

    "analytical":
        [
            "reasoning",
            "cognitive"
        ],

    # ---------------------------------
    # LEADERSHIP
    # ---------------------------------

    "leadership":
        [
            "leadership assessment",
            "management"
        ],

    "manager":
        [
            "people management",
            "leadership"
        ],

    # ---------------------------------
    # PERSONALITY
    # ---------------------------------

    "personality":
        [
            "behavioral assessment",
            "work style"
        ]
}


# =====================================
# QUERY SYNTHESIS
# =====================================

def synthesize_query(requirements):

    text = " ".join(requirements)

    text_lower = text.lower()

    expanded_terms = []

    # ---------------------------------
    # KEEP IMPORTANT TOKENS
    # ---------------------------------

    for token in text_lower.split():

        if token not in STOPWORDS:

            expanded_terms.append(token)

    # ---------------------------------
    # SEMANTIC EXPANSION
    # ---------------------------------

    for key, values in (
        NORMALIZATION_MAP.items()
    ):

        if key in text_lower:

            expanded_terms.extend(values)

    # ---------------------------------
    # REMOVE DUPLICATES
    # ---------------------------------

    final_terms = []

    seen = set()

    for term in expanded_terms:

        if term not in seen:

            final_terms.append(term)

            seen.add(term)

    return " ".join(final_terms)
