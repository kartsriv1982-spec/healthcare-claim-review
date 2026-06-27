
from datetime import datetime

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.models.schemas import DecisionRequest
from app.models.human_review import HumanReviewRequest

from app.services.s3_service import upload_claim_document
from app.services.textract_service import extract_text_from_s3

from app.database.db import get_db
from app.database.models import Claim

from app.database.audit_models import ClaimAuditLog
from app.langgraph.workflow import (
    build_workflow
)
from app.services.audit_service import log_audit

router = APIRouter()


# ==================================================
# Get All Claims
# ==================================================

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


# ==================================================
# Upload Claim
# ==================================================

@router.post("/upload")
async def upload_claim(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    try:

        print("=" * 60)
        print("UPLOAD CLAIM STARTED")
        print("=" * 60)

        file_key = upload_claim_document(file)

        claim_id = (
            f"CLM-"
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )

        claim = Claim(
            claim_id=claim_id,
            file_key=file_key,
            status="PROCESSING"
        )

        db.add(claim)

        # Push INSERT to DB but don't commit yet.
        db.flush()

        log_audit(

            db=db,

            claim_id=claim_id,

            stage="UPLOAD",

            actor="System",

            action="Claim Uploaded"
        )

        # Commit Claim + Audit together.
        db.commit()

        print("UPLOAD CLAIM COMPLETED")

        return {

            "claim_id": claim_id,

            "file_key": file_key,

            "status": "PROCESSING"
        }

    except Exception as ex:

        db.rollback()

        print("UPLOAD FAILED")
        print(ex)

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )

# ==================================================
# Get Claim
# ==================================================

@router.get("/{claim_id}")
def get_claim(claim_id: str):

    return {
        "claim_id": claim_id,
        "patient_name": "John Doe",
        "amount": 1200,
        "status": "REVIEW_READY"
    }


# ==================================================
# OCR Extraction
# ==================================================

@router.post("/{claim_id}/extract")
def extract_claim(
    claim_id: str,
    db: Session = Depends(get_db)
):

    try:

        print("=" * 60)
        print(f"OCR STARTED : {claim_id}")
        print("=" * 60)

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

        # ---------------------------------------
        # Extract OCR using Textract
        # ---------------------------------------

        text = extract_text_from_s3(

            bucket_name="healthcare-claim-documents-dev",

            file_key=claim.file_key
        )

        # ---------------------------------------
        # Update Claim
        # ---------------------------------------

        claim.extracted_text = text

        claim.extraction_status = "COMPLETED"

        claim.status = "OCR_COMPLETED"

        # Push update without committing
        db.flush()

        # ---------------------------------------
        # Audit Trail
        # ---------------------------------------

        log_audit(

            db=db,

            claim_id=claim.claim_id,

            stage="OCR",

            actor="AWS Textract",

            action="OCR Completed",

            workflow_stage="OCR_COMPLETED"
        )

        # ---------------------------------------
        # Commit Once
        # ---------------------------------------

        db.commit()

        print("OCR COMPLETED")

        return {

            "claim_id": claim_id,

            "status": "OCR_COMPLETED",

            "ocr_text": text
        }

    except HTTPException:

        db.rollback()

        raise

    except Exception as ex:

        db.rollback()

        print("=" * 60)
        print("OCR FAILED")
        print(ex)
        print("=" * 60)

        raise HTTPException(

            status_code=500,

            detail=f"OCR Extraction Failed : {str(ex)}"
        )
# ==================================================
# Load Claim Review Page
# ==================================================

@router.get("/{claim_id}/review")
def get_claim_review(
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

    return {

        "claim_id":
            claim.claim_id,

        "status":
            claim.status,

        "ocr_text":
            claim.extracted_text or
            "OCR not completed yet"
    }
# ==================================================
# Start AI Review
# ==================================================

@router.post("/{claim_id}/review")
def start_ai_review(
    claim_id: str,
    db: Session = Depends(get_db)
):

    try:

        print("=" * 60)
        print(f"AI REVIEW STARTED : {claim_id}")
        print("=" * 60)

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

        # ---------------------------------------
        # OCR must be completed
        # ---------------------------------------

        if not claim.extracted_text:

            raise HTTPException(
                status_code=400,
                detail="OCR not completed for this claim."
            )

        # ---------------------------------------
        # Execute LangGraph Workflow
        # ---------------------------------------

        workflow = build_workflow()

        result = workflow.invoke({

            "claim_id": claim.claim_id,

            "ocr_text": claim.extracted_text,

            "workflow_steps": []
        })

                # ---------------------------------------
        # Validation Failed
        # ---------------------------------------

        if not result["is_valid"]:

            claim.status = "VALIDATION_FAILED"

            db.flush()

            log_audit(

                db=db,

                claim_id=claim.claim_id,

                stage="VALIDATION",

                actor="Validation Agent",

                action="Validation Failed",

                workflow_stage="VALIDATION_FAILED",

                payload_json={

                    "missing_fields": result["missing_fields"]

                }
            )

            db.commit()

            return {

                "claim_id": claim.claim_id,

                "review_status": "VALIDATION_FAILED",

                "validation_status": False,

                "missing_fields": result["missing_fields"],

                "message": "Mandatory fields are missing."

            }
        # ==================================================
        # Persist AI Recommendation
        # ==================================================

        claim.ai_recommendation = result["recommendation"]

        claim.ai_confidence_score = result["confidence_score"]

        claim.ai_reasoning = result["policy_reasoning"]

        claim.requires_human_review = result["requires_human_review"]

        claim.current_workflow_stage = result["current_stage"]

        claim.status = "AI_REVIEW_COMPLETED"

        db.commit()

        print("========== LANGGRAPH RESULT ==========")
        print(result)
        print("======================================")

        # ---------------------------------------
        # Update Claim Master
        # ---------------------------------------

        claim.status = result["claim_status"]

        db.flush()

        # ---------------------------------------
        # Audit Trail
        # ---------------------------------------

        log_audit(

            db=db,

            claim_id=result["claim_id"],

            stage="POLICY_RECOMMENDATION",

            actor="Policy Agent",

            action=result["recommendation"],

            recommendation=result["recommendation"],

            confidence_score=result["confidence_score"],

            ai_reasoning=result["policy_reasoning"],

            retrieved_policy=result["retrieved_chunks"],

            workflow_stage=result["current_stage"],

            payload_json=result
        )

        # ---------------------------------------
        # Commit Everything
        # ---------------------------------------

        db.commit()

        print("AI REVIEW COMPLETED")

        return {

            "claim_id": result["claim_id"],

           "review_status": result["claim_status"],

            "workflow_stage": result["current_stage"],

            "workflow_steps": result["workflow_steps"],

            "validation_status": result["is_valid"],

            "missing_fields": result["missing_fields"],

            "recommendation": result["recommendation"],

            "confidence": result["confidence_score"],

            "summary": result["policy_reasoning"],

            "retrieved_chunks": result["retrieved_chunks"],

            "requires_human_review": result["requires_human_review"]
        }

    except HTTPException:

        db.rollback()

        raise

    except Exception as ex:

        db.rollback()

        print("=" * 60)
        print("AI REVIEW FAILED")
        print(ex)
        print("=" * 60)

        raise HTTPException(

            status_code=500,

            detail=f"AI Review Failed : {str(ex)}"
        )

# ==================================================
# Load Human Review Task
# ==================================================


def get_human_review_task(
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

    return {

        "claim_id": claim.claim_id,

        "review_status": claim.status,

        "assigned_to": claim.reviewed_by or "Not Assigned",

        "ai_recommendation": claim.ai_recommendation,

        "confidence": claim.ai_confidence_score,

        "summary": claim.ai_reasoning,

        "workflow_stage": claim.current_workflow_stage,

        "requires_human_review": claim.requires_human_review,

        "review_decision": claim.review_decision,

        "review_comments": claim.review_comments,

        "review_completed_date": claim.review_completed_date
    }


# ==================================================
# Submit Human Review
# ==================================================

@router.post("/{claim_id}/human-review")
def submit_human_review(
    claim_id: str,
    request: HumanReviewRequest,
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

    # ------------------------------------------
    # Update Claim
    # ------------------------------------------

    claim.review_decision = request.decision

    claim.review_comments = request.comments

    claim.reviewed_by = request.reviewed_by

    claim.review_completed_date = datetime.utcnow()

    if request.decision == "APPROVE":

        claim.status = "APPROVED"

    elif request.decision == "REJECT":

        claim.status = "REJECTED"

    else:

        claim.status = "REQUEST_INFO"

    db.flush()

    # ------------------------------------------
    # Audit Trail
    # ------------------------------------------

    log_audit(

        db=db,

        claim_id=claim.claim_id,

        stage="HUMAN_REVIEW",

        actor=request.reviewed_by,

        action=request.decision,

        workflow_stage="HUMAN_REVIEW_COMPLETED",

        payload_json={

            "comments": request.comments,

            "status": claim.status
        }
    )

    db.commit()

    return {

        "claim_id": claim.claim_id,

        "status": claim.status,

        "decision": request.decision,

        "reviewed_by": request.reviewed_by,

        "comments": request.comments
    }


# ==================================================
# Legacy Decision API
# ==================================================

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

# ==================================================
# Get Audit Trail
# ==================================================

@router.get("/{claim_id}/audit")
def get_audit_trail(
    claim_id: str,
    db: Session = Depends(get_db)
):

    claim = (
        db.query(Claim)
        .filter(Claim.claim_id == claim_id)
        .first()
    )

    if not claim:
        raise HTTPException(
            status_code=404,
            detail="Claim not found"
        )

    audit_logs = (
        db.query(ClaimAuditLog)
        .filter(
            ClaimAuditLog.claim_id == claim_id
        )
        .order_by(
            ClaimAuditLog.created_timestamp.asc()
        )
        .all()
    )

    return [

        {
            "log_id": log.log_id,

            "stage": log.stage,

            "actor": log.actor,

            "action": log.action,

            "recommendation": log.recommendation,

            "confidence_score": log.confidence_score,

            "ai_reasoning": log.ai_reasoning,

            "retrieved_policy": log.retrieved_policy,

            "workflow_stage": log.workflow_stage,

            "human_comments": log.human_comments,

            "payload_json": log.payload_json,

            "created_date": (
                log.created_timestamp.strftime(
                    "%d-%b-%Y %I:%M:%S %p"
                )
                if log.created_timestamp
                else None
            )
        }

        for log in audit_logs
    ]