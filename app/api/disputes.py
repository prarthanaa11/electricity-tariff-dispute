from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.models.contracts import DisputeRequest
from app.tasks import process_dispute


router = APIRouter(
    prefix="/api/v1/disputes",
    tags=["disputes"],
)


@router.post("")
def submit_dispute(
    request: DisputeRequest,
):
    run_id = str(uuid4())

    task = process_dispute.delay(
        run_id,
        request.model_dump(mode="json"),
    )

    return {
        "run_id": run_id,
        "task_id": task.id,
        "status": "queued",
        "message": (
            "The dispute was accepted for asynchronous processing."
        ),
    }


@router.get("/{run_id}")
def get_dispute_status(
    run_id: str,
):
    # Temporary implementation using the Celery result backend.
    # Replace with a durable PostgreSQL run record in the
    # final version.

    from app.core.celery_app import celery_app

    # The first implementation should use a mapping from
    # run_id to Celery task ID stored at submission time.
    # Do not assume run_id is the Celery task ID.

    raise HTTPException(
        status_code=501,
        detail=(
            "Run-status lookup must be connected to the "
            "persistent run registry."
        ),
    )