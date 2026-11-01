from typing import Any, TypedDict


class InvestigationState(TypedDict, total=False):
    run_id: str
    complaint: dict[str, Any]

    complaint_type: str
    extracted_facts: dict[str, Any]

    search_queries: list[str]
    evidence: list[dict[str, Any]]

    proposed_position: dict[str, Any]
    verification: dict[str, Any]

    route: str
    escalation_required: bool
    escalation_reason: str | None

    status: str
    errors: list[str]

    step_count: int
    tool_call_count: int
    prompt_version: str