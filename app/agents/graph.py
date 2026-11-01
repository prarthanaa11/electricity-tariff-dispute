from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from app.agents.state import InvestigationState
from app.agents.investigator import investigate
from app.agents.verifier import verify_evidence


def build_graph():
    graph = StateGraph(InvestigationState)

    graph.add_node(
        "investigator",
        investigate,
    )

    graph.add_node(
        "verifier",
        verify_evidence,
    )

    graph.add_edge(
        START,
        "investigator",
    )

    graph.add_edge(
        "investigator",
        "verifier",
    )

    graph.add_edge(
        "verifier",
        END,
    )

    return graph.compile()


def run_investigation(
    run_id: str,
    complaint: dict,
):
    workflow = build_graph()

    initial_state = {
        "run_id": run_id,
        "complaint": complaint,
        "evidence": [],
        "errors": [],
        "step_count": 0,
        "tool_call_count": 0,
        "prompt_version": "v1",
        "status": "started",
    }

    return workflow.invoke(
        initial_state,
        config={
            "recursion_limit": 8,
        },
    )
def route_after_verification(state):
    if state.get("escalation_required"):
        if state.get("step_count", 0) < 3:
            return "investigator"

        return "escalate"

    return "finalize"