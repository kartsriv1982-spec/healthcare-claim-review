from fastapi import APIRouter, UploadFile, File
from app.data.mock_data import CLAIMS
from app.models.schemas import DecisionRequest
from app.services.s3_service import upload_claim_document
from datetime import datetime

router = APIRouter()
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import Claim
from app.services.textract_service import (
    extract_text_from_s3
)

@router.get("")
def get_claims(
    db: Session = Depends(get_db)
):

    claims = db.query(Claim).all()

    response = []

    for claim in claims:

        response.append({
            "claim_id": claim.claim_id,
            "file_key": claim.file_key,
            "status": claim.status,
            "created_date": claim.created_date
        })

    return response




@router.post("/upload")
async def upload_claim(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    file_key = upload_claim_document(file)

    claim_id = f"CLM-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    claim = Claim(
        claim_id=claim_id,
        file_key=file_key,
        status="PROCESSING"
    )

    db.add(claim)

    db.commit()

    return {
        "claim_id": claim_id,
        "file_key": file_key,
        "status": "PROCESSING"
    }

@router.get("/{claim_id}")
def get_claim(claim_id: str):

    return {
        "claim_id": claim_id,
        "patient_name": "John Doe",
        "amount": 1200,
        "status": "REVIEW_READY"
    }


@router.get("/{claim_id}/review")
def review_claim(claim_id: str):

    return {
        "claim_id": claim_id,
        "recommendation": "APPROVE",
        "confidence": 92
    }


@router.post("/{claim_id}/decision")
def submit_decision(
    claim_id: str,
    request: DecisionRequest
    ):
    return {
        "claim_id": claim_id,
        "status": "CLOSED",
        "decision": request.decision
    }
    
@router.post("/{claim_id}/extract")
def extract_claim(
    claim_id: str,
    db: Session = Depends(get_db)
):

    claim = (
        db.query(Claim)
        .filter(
            Claim.claim_id == claim_id
        )
        .first()
    )

    if not claim:
        raise HTTPException(
            status_code=404,
            detail="Claim not found"
        )

    text = extract_text_from_s3(
        bucket_name="healthcare-claim-documents-dev",
        file_key=claim.file_key
    )

    claim.extracted_text = text

    claim.extraction_status = "COMPLETED"

    claim.status = "OCR_COMPLETED"

    db.commit()

    return {
        "claim_id": claim_id,
        "status": "OCR_COMPLETED"
    }