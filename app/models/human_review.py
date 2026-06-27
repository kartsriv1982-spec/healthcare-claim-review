from pydantic import BaseModel


class HumanReviewRequest(BaseModel):
    decision: str
    comments: str
    reviewed_by: str


class HumanReviewResponse(BaseModel):
    claim_id: str
    status: str
    decision: str
    reviewed_by: str
    comments: str