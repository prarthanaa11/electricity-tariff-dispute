import json
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.models.contracts import DisputeRequest


app = FastAPI(
    title="Electricity Tariff Dispute Triage Service",
    version="0.2.0",
)

QUARANTINE_DIR = Path("data/quarantine")
QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)


def quarantine_record(payload, errors):
    record_id = str(uuid4())

    record = {
        "record_id": record_id,
        "payload": payload,
        "errors": errors,
        "agent_started": False,
    }

    path = QUARANTINE_DIR / f"{record_id}.json"
    path.write_text(
        json.dumps(record, indent=2, default=str),
        encoding="utf-8",
    )

    return record_id


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    try:
        payload = await request.json()
    except Exception:
        payload = {
            "unreadable_request": True,
        }

    errors = [
        {
            "field": ".".join(
                str(part) for part in error["loc"]
            ),
            "message": error["msg"],
            "type": error["type"],
        }
        for error in exc.errors()
    ]

    quarantine_id = quarantine_record(
        payload,
        errors,
    )

    return JSONResponse(
        status_code=422,
        content={
            "status": "rejected",
            "quarantine_id": quarantine_id,
            "agent_started": False,
            "errors": errors,
        },
    )


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "tariff-api",
    }


@app.post("/api/v1/disputes/validate")
def validate_dispute(request: DisputeRequest):
    return {
        "status": "validated",
        "agent_started": False,
        "complaint": request.model_dump(mode="json"),
    }