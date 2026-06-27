import requests

RAG_URL = "http://localhost:8002/RAG/query"


def policy_agent(state):

    state["current_stage"] = "POLICY_AGENT_STARTED"

    question = f"""
Claim Details:

{state["ocr_text"]}

Based on the above claim, determine whether the claim is covered under the policy.
"""

    payload = {
        "question": question,
        "plan_name": "CORPORATE HEALTH ELITE",
        "rule_type": "coverage",
        "top_k": 5
    }

    response = requests.post(
        RAG_URL,
        json=payload,
        timeout=60
    )

    #response.raise_for_status()

    #rag_result = response.json()

    try:
        response.raise_for_status()

        rag_result = response.json()

    except Exception as ex:

        state["current_stage"] = "POLICY_AGENT_FAILED"

        raise Exception(
            f"Policy Agent failed: {str(ex)}"
        )

    print("========== RAG RESPONSE ==========")
    print(rag_result)
    print("==================================")

    # ==================================================
    # Policy Recommendation
    # ==================================================

    state["recommendation"] = rag_result["coverage_decision"]

    state["confidence_score"] = rag_result["confidence_score"]

    state["policy_reasoning"] = rag_result["reasoning"]

    # ==================================================
    # Policy Evidence
    # ==================================================

    state["policy_clause"] = rag_result["policy_clause"]

    state["matched_section"] = rag_result["matched_section"]

    state["medical_necessity"] = rag_result["medical_necessity"]

    state["exclusion"] = rag_result["exclusion"]

    state["retrieved_chunks"] = rag_result["retrieved_chunks"]

    state["current_stage"] = "POLICY_AGENT_COMPLETED"

    return state