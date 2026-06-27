from sqlalchemy.orm import Session

from app.database.audit_models import ClaimAuditLog


def log_audit(
    db: Session,
    claim_id: str,
    stage: str,
    actor: str,
    action: str,
    recommendation: str = None,
    confidence_score: float = None,
    ai_reasoning: str = None,
    retrieved_policy=None,
    human_comments: str = None,
    workflow_stage: str = None,
    payload_json=None,
    processor_id: int = None
):

    audit = ClaimAuditLog(

        claim_id=claim_id,

        processor_id=processor_id,

        stage=stage,

        actor=actor,

        action=action,

        recommendation=recommendation,

        confidence_score=confidence_score,

        ai_reasoning=ai_reasoning,

        retrieved_policy=retrieved_policy,

        human_comments=human_comments,

        workflow_stage=workflow_stage,

        payload_json=payload_json
    )

    db.add(audit)

    # IMPORTANT
    # No commit here.
    # Caller will commit.