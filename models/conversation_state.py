def initialize_state():

    return {

        "requirements": [],

        "last_recommendations": []
    }


def merge_state(
    current_state,
    user_query
):

    current_state[
        "requirements"
    ].append(user_query)

    return current_state
