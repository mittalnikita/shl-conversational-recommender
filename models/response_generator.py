import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "llama-3.1-8b-instant"

class ResponseGenerator:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

    def generate_recommendation_response(
        self,
        user_query,
        recommendations
    ):

        if not recommendations:

            return (
                "I could not find suitable "
                "SHL assessments for the "
                "given requirements."
            )

        recommendation_text = ""

        for idx, item in enumerate(
            recommendations[:3],
            start=1
        ):

            explanation = " ".join(
                item.get(
                    "explanation",
                    []
                )
            )

            recommendation_text += (
                f"{idx}. "
                f"{item['name']}\n"
                f"Explanation: "
                f"{explanation}\n\n"
            )

        prompt = f"""
    You are an SHL assessment recommendation assistant.

    User Request:
    {user_query}

    Recommendations:
    {recommendation_text}

    Generate a concise, professional, conversational response.

    STRICT RULES:
    - Only discuss provided assessments
    - Do not invent capabilities
    - Do not generalize beyond descriptions
    - Keep response concise
    - Ground every statement in catalog data
    - Keep the tone professional
    - Do not mention assessments not provided
    - Do not repeat assessment descriptions verbatim
    - Keep explanations specific

    Return a natural conversational response.
    """

        response = (
            self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=300
            )
        )

        return (
            response
            .choices[0]
            .message.content
        )
    
    def generate_comparison_response(
        self,
        user_query,
        comparisons
    ):

        prompt = f"""
    You are an SHL assessment recommendation assistant.

    The user asked:
    {user_query}

    Below are grounded assessment comparison details:

    {comparisons}

    Generate a natural comparison explaining:

    - key differences
    - best use cases
    - leadership vs technical suitability
    - hiring scenarios
    - remote testing support
    - seniority suitability

    Do not invent information.
    Use only the provided grounded data.
    Keep the response recruiter-friendly.
    """

        response = (
            self.client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.3
            )
        )

        return (
            response
            .choices[0]
            .message.content
        )