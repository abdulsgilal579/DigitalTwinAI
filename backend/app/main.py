from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.routes.github import router as github_router
from app.routes.profile import router as profile_router
from app.routes.voice import router as voice_router
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(title="Digital Twin API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile_router, prefix="/profile", tags=["profile"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(github_router, prefix="/github", tags=["github"])
app.include_router(voice_router, prefix="/voice", tags=["voice"])



@app.get("/health")
def health():
    return {"status": "ok", "service": "Digital Twin API"}