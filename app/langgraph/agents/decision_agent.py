def decision_agent(state):

    # ==================================================
    # Decision Agent
    # ==================================================

    print("Decision Agent Executed")

    state["current_stage"] = "DECISION_AGENT_STARTED"

    recommendation = state["recommendation"]

    confidence = state["confidence_score"]

    # --------------------------------------------------
    # Business Decision
    # --------------------------------------------------

    # For this capstone every AI decision
    # goes through Human Review (HIL)

    state["requires_human_review"] = True

    if state["requires_human_review"]:

        state["claim_status"] = "PENDING_HUMAN_REVIEW"

    else:

        if recommendation == "APPROVE":

            state["claim_status"] = "APPROVED"

        else:

            state["claim_status"] = "REJECTED"

    # --------------------------------------------------
    # Workflow Tracking
    # --------------------------------------------------

    state["workflow_steps"].append(
        "Decision Generated"
    )

    state["current_stage"] = "DECISION_AGENT_COMPLETED"

    return state