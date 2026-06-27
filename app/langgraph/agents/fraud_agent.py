def fraud_agent(state):

    state["fraud_result"] = (
        "No fraud indicators detected"
    )

    print("Fraud Agent Executed")

    state["workflow_steps"].append(
    "Fraud Assessment Completed"
)

    return state