from fastapi import APIRouter
from app.models.schemas import LoginRequest

router = APIRouter()


@router.post("/login")
def login(request: LoginRequest):

    return {
        "access_token": "mock-token",
        "token_type": "Bearer",
        "role": "CLAIMS_ADJUSTER"
    }