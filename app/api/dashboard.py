from fastapi import APIRouter

router = APIRouter()


@router.get("/metrics")
def metrics():

    return {
        "total_claims": 325,
        "pending_review": 24,
        "approved_today": 87,
        "rejected_today": 13
    }