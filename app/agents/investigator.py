from app.agents.tools import (
    lookup_request_fields,
    search_corpus,
)
from app.agents.state import InvestigationState


def investigate(
    state: InvestigationState,
) -> InvestigationState:
    complaint = state["complaint"]

    facts = lookup_request_fields(complaint)

    queries = [
        complaint["complaint_text"],
        (
            "Applicable tariff category definition for "
            f'{facts.get("premises_type", "unknown")} premises'
        ),
        (
            "Rules for mixed domestic and commercial use, "
            "change of premises use, and re-categorisation"
        ),
    ]

    evidence = []

    for query in queries:
        if state.get("tool_call_count", 0) >= 12:
            break

        results = search_corpus(query)

        state["tool_call_count"] = (
            state.get("tool_call_count", 0) + 1
        )

        evidence.extend(results)

    # Deduplicate by chunk ID.
    unique_evidence = {}

    for item in evidence:
        unique_evidence[item["chunk_id"]] = item

    return {
        **state,
        "extracted_facts": facts,
        "search_queries": queries,
        "evidence": list(unique_evidence.values()),
        "step_count": state.get("step_count", 0) + 1,
        "status": "investigated",
    }