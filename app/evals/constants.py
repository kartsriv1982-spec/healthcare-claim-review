from enum import Enum

class ClaimDecision(Enum):

    APPROVED="APPROVED"

    FRAUD="REJECTED_FRAUD"

    NIGO="NIGO"

    HUMAN_REVIEW="HUMAN_REVIEW"

class AgentName(Enum):

    OCR = "OCR Agent"

    VALIDATION="Validation Agent"

    RECOMMENDATION="Recommendation Agent"

    
class ToolName(Enum):

    POLICY_SEARCH="Policy Search"

    CLAIM_HISTORY="Claims History"

    COVERAGE_CALCULATOR="Coverage Calculator"

    FRAUD_LOOKUP="Fraud Lookup"