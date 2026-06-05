from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.groq_service import ask_groq

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


PROFILE_CONTEXT = """
Name: Abdul Samad Gilal
Background: Computer Systems Engineering graduate, MS Computer Science student,
AI Engineer, Full Stack Developer, and Researcher.
Primary interests: Agentic AI, RAG, FastAPI, AWS, Machine Learning, Data Science,
LLM Evaluation, and Research.
Project: DigitalTwinAI, a voice-enabled AI digital twin powered by GitHub, RAG,
FastAPI, Groq, and ElevenLabs.
"""


@router.post("/")
def chat(request: ChatRequest):
    try:
        answer = ask_groq(request.message, PROFILE_CONTEXT)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "question": request.message,
        "answer": answer,
    }
