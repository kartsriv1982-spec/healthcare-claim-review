from pydantic import BaseModel
from typing import Dict, List, Any
from pathlib import Path

class GroundTruth(BaseModel):

    claim_id: str

    expected_decision: str

    expected_reasons: List[str]

    expected_tools: List[str]

    expected_rag_documents: List[str]

    expected_human_review: bool

class AgentResult(BaseModel):

    claim_id: str

    decision: str

    reasons: List[str]

    confidence: float

    fraud_score: float

    eligible_amount: float

    tools_used: List[str]

    retrieved_documents: List[str]

    execution_time: float

    token_usage: Dict[str, Any]

class ToolTrace(BaseModel):

    tool_name: str

    input: str

    output: str

    latency: float

    success: bool

class RetrievalTrace(BaseModel):

    query: str

    retrieved_documents: List[str]

    retrieved_chunks: List[str]

    similarity_scores: List[float]

class AgentTrace(BaseModel):

    agent_name: str

    input_summary: str

    output_summary: str

    execution_time: float

    tools: List[ToolTrace]

class EvaluationResult(BaseModel):

    claim_id: str

    decision_score: float

    fraud_score: float

    tool_score: float

    rag_score: float

    guardrail_score: float

    workflow_score: float

    overall_score: float

    passed: bool

from datetime import datetime


class DriftRecord(BaseModel):

    timestamp: datetime

    decision_accuracy: float

    fraud_accuracy: float

    rag_accuracy: float

    tool_accuracy: float

    hallucination_rate: float

class EvaluationSession(BaseModel):

    session_id: str

    started_at: datetime

    finished_at: datetime

    total_claims: int

    passed: int

    failed: int

    results: List[EvaluationResult]

class EvaluationSummary(BaseModel):

    overall_accuracy: float

    fraud_accuracy: float

    nigo_accuracy: float

    approval_accuracy: float

    tool_accuracy: float

    rag_accuracy: float

    latency: float

    average_confidence: float

class ClaimPackage(BaseModel):

    claim_id: str

    category: str

    folder: Path

    documents: dict[str, Path]

    ground_truth: GroundTruth | None = None

