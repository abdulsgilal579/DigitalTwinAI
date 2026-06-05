from fastapi import APIRouter, HTTPException

from app.services.github_service import fetch_repositories

router = APIRouter()


@router.get("/repos")
async def get_repositories():
    try:
        repositories = await fetch_repositories()
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {"repositories": repositories}