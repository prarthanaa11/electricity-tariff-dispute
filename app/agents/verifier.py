from app.agents.state import InvestigationState


ALLOWED_ROUTES = {
    "bill-stands-with-reason",
    "revision-recommended",
    "site-inspection-required",
}


def verify_evidence(
    state: InvestigationState,
) -> InvestigationState:
    evidence = state.get("evidence", [])

    errors = []

    if not evidence:
        errors.append("No supporting passages retrieved.")

    valid_chunks = {
        item["chunk_id"]: item
        for item in evidence
        if item.get("chunk_id") and item.get("text")
    }

    if len(valid_chunks) != len(evidence):
        errors.append(
            "One or more passages lack a valid chunk ID or text."
        )

    complaint = state["complaint"]

    premises_type = complaint.get("premises_type")

    mixed_use_evidence = any(
        any(
            term in item["text"].lower()
            for term in [
                "mixed use",
                "mixed-use",
                "commercial purpose",
                "non-domestic",
                "partly",
            ]
        )
        for item in evidence
    )

    # This is a conservative evidence-coverage check,
    # not a legal interpretation of the documents.
    needs_human_review = (
        premises_type == "mixed_use"
        and not mixed_use_evidence
    )

    escalation_required = (
        bool(errors)
        or needs_human_review
    )

    if errors:
        reason = "Evidence verification failed."
    elif needs_human_review:
        reason = (
            "The mixed-use issue is not sufficiently covered "
            "by the retrieved evidence."
        )
    else:
        reason = None

    return {
        **state,
        "verification": {
            "passed": not escalation_required,
            "errors": errors,
            "evidence_count": len(valid_chunks),
            "mixed_use_evidence_found": mixed_use_evidence,
        },
        "escalation_required": escalation_required,
        "escalation_reason": reason,
        "status": (
            "escalated"
            if escalation_required
            else "verified"
        ),
    }