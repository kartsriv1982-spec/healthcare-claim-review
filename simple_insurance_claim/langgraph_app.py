"""
langgraph_app.py
-----------------
Main file. Builds a simple 3-step LangGraph workflow:

    OCR Agent -> Validation Agent -> Recommendation Agent

Run it like this:
    python langgraph_app.py sample_claims/sample_claim.png
"""

import sys
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

from Agents.OCR_Agent import ocr_agent_node
from Agents.Validation_Agent import validation_agent_node
from Agents.Recommendation import recommendation_agent_node

load_dotenv()


# This just describes what fields can live in our shared "state" dictionary.
# Every agent reads from / writes to this same dictionary as it moves
# through the graph.
class ClaimState(TypedDict, total=False):
    document_path: str
    ocr_text: str
    claim_number: Optional[str]
    claim_amount: Optional[str]
    is_valid: bool
    validation_reasons: list
    recommendation: str
    reasoning: str


# 1. Create the graph
workflow = StateGraph(ClaimState)

# 2. Add each agent as a node
workflow.add_node("ocr_agent", ocr_agent_node)
workflow.add_node("validation_agent", validation_agent_node)
workflow.add_node("recommendation_agent", recommendation_agent_node)

# 3. Connect the nodes in a simple straight line
workflow.set_entry_point("ocr_agent")
workflow.add_edge("ocr_agent", "validation_agent")
workflow.add_edge("validation_agent", "recommendation_agent")
workflow.add_edge("recommendation_agent", END)

# 4. Compile it into a runnable app
app = workflow.compile()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python langgraph_app.py <path_to_claim_image.png>")
        sys.exit(1)

    document_path = sys.argv[1]

    try:
        # This is the starting state we feed into the graph
        initial_state = {"document_path": document_path}
        final_state = app.invoke(initial_state)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while running the workflow: {e}")
        sys.exit(1)

    print("\n----- FINAL RESULT -----")
    print("Claim Number   :", final_state.get("claim_number"))
    print("Claim Amount   :", final_state.get("claim_amount"))
    print("Is Valid       :", final_state.get("is_valid"))
    print("Reasons        :", final_state.get("validation_reasons"))
    print("Recommendation :", final_state.get("recommendation"))
    print("Reasoning      :", final_state.get("reasoning"))
