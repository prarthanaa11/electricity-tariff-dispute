from app.agents.state import InvestigationState


def escalate(
    state: InvestigationState,
) -> InvestigationState:
    return {
        **state,
        "route": "human-review",
        "escalation_required": True,
        "status": "escalated",
        "proposed_position": {
            "determination": None,
            "reason": (
                state.get("escalation_reason")
                or "Insufficient verified evidence."
            ),
            "human_review_required": True,
        },
    }