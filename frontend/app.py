import streamlit as st
import requests


API_URL = ("http://127.0.0.1:8000/chat")


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="SHL Assessment Assistant",
    layout="wide"
)

st.markdown("""
<style>

    .stExpander {
        border-radius: 10px;
        border: 1px solid #444;
    }

</style>
""", unsafe_allow_html=True)


st.title("SHL Conversational Assessment Assistant")
st.markdown("AI-powered SHL assessment recommendation system.")

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.header("System Capabilities")

    st.markdown("""
    - Conversational assessment recommendations
    - Assessment comparison
    - Explanation generation
    - Conversational refinement
    - Catalog-grounded responses
    - Multi-turn interaction support
    """)


# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =====================================
# CHAT HISTORY RENDERING
# =====================================

for message in (
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =====================================
# USER INPUT
# =====================================

user_input = st.chat_input(
    "Ask about SHL assessments..."
)


if user_input:

    # ---------------------------------
    # ADD USER MESSAGE
    # ---------------------------------

    st.session_state.messages.append({

        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):

        st.markdown(user_input)

    # ---------------------------------
    # CALL BACKEND
    # ---------------------------------

    payload = {
        "messages":
            st.session_state.messages
    }

    with st.spinner( "Generating response..." ):

        response = requests.post(
            API_URL,
            json=payload
        )

    result = response.json()

    # ---------------------------------
    # BUILD ASSISTANT RESPONSE
    # ---------------------------------

    assistant_response = ""

    status = result.get(
        "status",
        ""
    )

    # =================================
    # SUCCESS RECOMMENDATION FLOW
    # =================================

    if status == "success":

        assistant_response += (
            result.get(
                "response",
                ""
            )
        )

        recommendations = (
            result.get(
                "recommendations",
                []
            )
        )

    
        with st.chat_message("assistant"):

            st.markdown(
                assistant_response
            )

            for item in recommendations:

                with st.expander(
                    item["name"]
                ):

                    st.markdown(
                        item["description"]
                    )

                    st.markdown(
                        f"**Remote Testing:** "
                        f"{item['remote_testing']}"
                    )

                    st.markdown(
                        f"**Adaptive Support:** "
                        f"{item['adaptive_support']}"
                    )

                    st.markdown(
                        f"**Job Levels:** "
                        f"{', '.join(item['job_levels'])}"
                    )

                    st.markdown(
                        "**Why Recommended:**"
                    )

                    for explanation in (
                        item.get(
                            "explanation",
                            []
                        )
                    ):

                        st.markdown(
                            f"- {explanation}"
                        )

                    st.markdown(
                        f"[SHL Link]"
                        f"({item['url']})"
                    )



    # =================================
    # EXPLANATION FLOW
    # =================================

    elif status == "explanation":

        assistant_response += (
            result.get(
                "response",
                ""
            )
        )

    # =================================
    # COMPARISON FLOW
    # =================================

    elif status == "comparison":

        assistant_response += (
            result.get(
                "response",
                ""
            )
        )

    # =================================
    # QA FLOW
    # =================================

    elif status == "qa_response":

        assistant_response += (
            result.get(
                "response",
                ""
            )
        )

    # =================================
    # CLARIFICATION FLOW
    # =================================

    elif status == "clarification_needed":

        assistant_response += (
            result["policy"]["message"]
        )

    # =================================
    # REJECTION FLOW
    # =================================

    elif status == "rejected":

        assistant_response += (
            result["policy"]["message"]
        )

    # =================================
    # FALLBACK
    # =================================

    else:
        assistant_response += (
            "Something went wrong."
        )


    # ---------------------------------
    # DISPLAY ASSISTANT RESPONSE
    # ---------------------------------

    if status != "success":

        with st.chat_message(
            "assistant"
        ):

            st.markdown(
                assistant_response
            )


    # ---------------------------------
    # SAVE ASSISTANT MESSAGE
    # ---------------------------------

    st.session_state.messages.append({

        "role": "assistant",
        "content": assistant_response
    })