from fastapi import APIRouter, HTTPException
import httpx
from app.services.voice_service import get_elevenlabs_signed_url
from pydantic import BaseModel
from app.services.github_service import fetch_repositories
from app.services.groq_service import ask_groq
from app.services.profile_service import build_profile_context

router = APIRouter()

class VoiceAskRequest(BaseModel):
    question: str

@router.get("/signed-url")
async def create_signed_url():
    try:
        signed_url = await get_elevenlabs_signed_url()
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail={
                "message": "ElevenLabs signed URL request failed.",
                "status_code": exc.response.status_code,
                "response": exc.response.text,
            },
        ) from exc

    return {"signed_url": signed_url}

@router.post("/ask")
async def ask_voice_agent(request: VoiceAskRequest):
    try:
        profile_context = build_profile_context()
        repositories = await fetch_repositories()

        github_context = "\n".join(
            [
                f"- {repo['name']}: {repo['description']} "
                f"Language: {repo['language']}. "
                f"Stars: {repo['stars']}. "
                f"URL: {repo['url']}"
                for repo in repositories
            ]
        )

        full_context = f"""
{profile_context}

GitHub repositories:
{github_context}
"""

        answer = ask_groq(request.question, full_context)

    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
    "answer": answer,
    "result": answer,
    "message": answer,    }