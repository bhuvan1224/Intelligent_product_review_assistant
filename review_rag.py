from groq import Groq
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_reviews(phone_name, reviews):

    prompt = f"""
    Analyze these reviews for {phone_name}.

    Reviews:
    {chr(10).join(reviews)}

    Give:
    1. Overall sentiment
    2. Strengths
    3. Weaknesses
    4. Final recommendation

    Use simple human-readable language.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content