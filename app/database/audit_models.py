from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import JSONB

from datetime import datetime

from app.database.models import Base


class ClaimAuditLog(Base):

    __tablename__ = "claim_audit_logs"

    log_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    claim_id = Column(
        String,
        ForeignKey("claims_master.claim_id"),
        nullable=False
    )

    processor_id = Column(
        Integer,
        nullable=True
    )

    stage = Column(
        String,
        nullable=False
    )

    actor = Column(
        String,
        nullable=False
    )

    action = Column(
        String,
        nullable=False
    )

    recommendation = Column(
        String,
        nullable=True
    )

    confidence_score = Column(
        Float,
        nullable=True
    )

    ai_reasoning = Column(
        Text,
        nullable=True
    )

    retrieved_policy = Column(
        JSONB,
        nullable=True
    )

    human_comments = Column(
        Text,
        nullable=True
    )

    workflow_stage = Column(
        String,
        nullable=True
    )

    payload_json = Column(
        JSONB,
        nullable=True
    )

    created_timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )