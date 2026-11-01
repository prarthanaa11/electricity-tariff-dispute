from typing import Literal

from pydantic import BaseModel, Field


Route = Literal[
    "bill-stands-with-reason",
    "revision-recommended",
    "site-inspection-required",
]


class EvidenceCitation(BaseModel):
    document_id: str
    document_name: str
    page: int = Field(ge=1)

    clause_id: str | None = None

    chunk_id: str
    quoted_text: str = Field(
        min_length=1,
        max_length=3000,
    )


class TriageResult(BaseModel):
    run_id: str
    status: Literal[
        "completed",
        "escalated",
        "failed",
    ]

    complaint_type: str

    recommended_route: Route | None = None

    tariff_position: str | None = None

    explanation: str

    citations: list[EvidenceCitation] = []

    verification_passed: bool

    escalation_required: bool

    escalation_reason: str | None = None

    prompt_version: str