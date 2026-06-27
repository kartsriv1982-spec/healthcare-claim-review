def human_review_agent(state):

    print("Human Review Agent Executed")

    state["current_stage"] = "HUMAN_REVIEW_PENDING"

    state["workflow_steps"].append(
        "Human Review Pending"
    )

    # Do not overwrite the Policy Agent output.
    # Recommendation, confidence, and reasoning
    # are already populated by the Policy Agent.

    state["requires_human_review"] = True

    return state