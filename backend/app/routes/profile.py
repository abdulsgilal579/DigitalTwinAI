from fastapi import APIRouter, HTTPException

from app.services.profile_service import load_profile

router = APIRouter()


@router.get("/")
def get_profile():
    try:
        profile = load_profile()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail="Profile data file not found.") from exc

    return profile