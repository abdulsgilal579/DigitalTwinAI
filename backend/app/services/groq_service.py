from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL


def ask_groq(question: str, context: str) -> str:
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are DigitalTwinAI, the AI digital twin of Abdul Samad "
                    "Gilal. Answer using only the provided context. If the "
                    "answer is not available in the context, say that the "
                    "information is not available yet."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}",
            },
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content
