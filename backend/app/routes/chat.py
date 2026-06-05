from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.github_service import fetch_repositories
from app.services.groq_service import ask_groq
from app.services.profile_service import build_profile_context

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


PROFILE_CONTEXT = build_profile_context()

@router.post("/")
async def chat(request: ChatRequest):
    try:
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
                        {PROFILE_CONTEXT}
                        GitHub repositories:
                        {github_context}
                        """

        answer = ask_groq(request.message, full_context)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "question": request.message,
        "answer": answer,
    }