from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.routes.github import router as github_router

app = FastAPI(title="Digital Twin API", version="1.0.0")

app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(github_router, prefix="/github", tags=["github"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "Digital Twin API"}