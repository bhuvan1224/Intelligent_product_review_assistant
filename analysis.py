import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY")
)


def analyze_product(
    selected_phone,
    recommended_phone,
    budget,
    priority
):

    prompt = f"""
You are a smartphone expert.

Selected Phone:
{selected_phone}

Recommended Phone:
{recommended_phone}

Budget:
₹{budget}

Priority:
{priority}

Compare both phones.

Provide:

📷 Camera Winner
🔋 Battery Winner
🎮 Gaming Winner
💾 Storage Winner
📺 Display Winner
💰 Value For Money Winner

Then give:

👍 Why Selected Phone Is Good

👍 Why Recommended Phone Is Good

🎯 Final Verdict

Rules:
- English only
- Maximum 150 words
- Use bullet points
- Keep concise
"""

    try:

        response = llm.invoke(prompt)

        return response.content

    except Exception as e:

        return f"Error: {str(e)}"