from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    String,
    Text
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Claim(Base):

    __tablename__ = "claims_master"

    # ==================================================
    # Claim Information
    # ==================================================

    claim_id = Column(
        String,
        primary_key=True
    )

    file_key = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    created_date = Column(
        DateTime,
        default=datetime.utcnow
    )

    # ==================================================
    # OCR Information
    # ==================================================

    extracted_text = Column(
        Text,
        nullable=True
    )

    extraction_status = Column(
        String,
        nullable=True
    )

    # ==================================================
    # AI Recommendation
    # ==================================================

    ai_recommendation = Column(
        String(30),
        nullable=True
    )

    ai_confidence_score = Column(
        Float,
        nullable=True
    )

    ai_reasoning = Column(
        Text,
        nullable=True
    )

    requires_human_review = Column(
        Boolean,
        default=True
    )

    current_workflow_stage = Column(
        String(100),
        nullable=True
    )

    # ==================================================
    # Human Review
    # ==================================================

    review_decision = Column(
        String(30),
        nullable=True
    )

    review_comments = Column(
        Text,
        nullable=True
    )

    reviewed_by = Column(
        String(100),
        nullable=True
    )

    review_completed_date = Column(
        DateTime,
        nullable=True
    )