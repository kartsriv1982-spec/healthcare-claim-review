"""
Validation_Agent.py
--------------------
Agent 2: Validates the claim using simple, hardcoded business rules.
No RAG, no vector store, no LLM calls — just plain Python checks.

Rules:
- claim_number and claim_amount must be present.
- claim_amount must be a number and not exceed a fixed policy limit.
"""

MAX_CLAIM_AMOUNT = 100000  # simple fixed policy limit for this demo


def validate_claim(claim_number, claim_amount) -> dict:
    reasons = []

    if not claim_number:
        reasons.append("Claim number is missing.")

    if not claim_amount:
        reasons.append("Claim amount is missing.")
    else:
        try:
            amount = float(claim_amount)
            if amount > MAX_CLAIM_AMOUNT:
                reasons.append(f"Claim amount {amount} exceeds policy limit of {MAX_CLAIM_AMOUNT}.")
        except ValueError:
            reasons.append("Claim amount is not a valid number.")

    is_valid = len(reasons) == 0
    return {
        "is_valid": is_valid,
        "validation_reasons": reasons,
    }


# ---- LangGraph node ----
def validation_agent_node(state: dict) -> dict:
    print("Running Validation Agent...")
    result = validate_claim(state.get("claim_number"), state.get("claim_amount"))

    state["is_valid"] = result["is_valid"]
    state["validation_reasons"] = result["validation_reasons"]
    return state


if __name__ == "__main__":
    # Quick manual test
    print(validate_claim("CLM-001", "45000"))
    print(validate_claim(None, "999999"))
