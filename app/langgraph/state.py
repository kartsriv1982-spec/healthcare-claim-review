from typing import TypedDict


class ClaimReviewState(TypedDict):

    # ==========================================
    # Claim Information
    # ==========================================

    claim_id: str

    ocr_text: str

    # ==========================================
    # Workflow Tracking
    # ==========================================

    workflow_steps: list[str]

    current_stage: str

    # ==========================================
    # Validation Agent
    # ==========================================

    is_valid: bool

    missing_fields: list

    validation_result: str

    # ==========================================
    # Policy Recommendation Agent (RAG)
    # ==========================================

    recommendation: str

    confidence_score: float

    policy_reasoning: str

    policy_clause: str

    matched_section: str

    medical_necessity: bool

    exclusion: str

    retrieved_chunks: list[str]

    # ==========================================
    # Human Review
    # ==========================================

    requires_human_review: bool
    claim_status: str