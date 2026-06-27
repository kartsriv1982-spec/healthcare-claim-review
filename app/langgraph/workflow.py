from langgraph.graph import StateGraph
from langgraph.graph import END

from app.langgraph.state import ClaimReviewState

from app.langgraph.agents.validation_agent import (
    validation_agent
)

from app.langgraph.agents.policy_agent import (
    policy_agent
)

from app.langgraph.agents.decision_agent import (
    decision_agent
)

from app.langgraph.router import (
    route_validation
)


def build_workflow():

    workflow = StateGraph(
        ClaimReviewState
    )

    # ==================================================
    # Register Nodes
    # ==================================================

    workflow.add_node(
        "validation",
        validation_agent
    )

    workflow.add_node(
        "policy",
        policy_agent
    )

    workflow.add_node(
        "decision",
        decision_agent
    )

    # ==================================================
    # Entry Point
    # ==================================================

    workflow.set_entry_point(
        "validation"
    )

    # ==================================================
    # Validation Routing
    # ==================================================

    workflow.add_conditional_edges(

        "validation",

        route_validation,

        {

            "VALID": "policy",

            "INVALID": END
        }
    )

    # ==================================================
    # Workflow Sequence
    # ==================================================

    workflow.add_edge(

        "policy",

        "decision"
    )

    workflow.add_edge(

        "decision",

        END
    )

    return workflow.compile()