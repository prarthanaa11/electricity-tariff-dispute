from celery import shared_task

from app.agents.graph import run_investigation


@shared_task(
    bind=True,
    name="tariff.process_dispute",
)
def process_dispute(
    self,
    run_id: str,
    complaint: dict,
):
    result = run_investigation(
        run_id=run_id,
        complaint=complaint,
    )

    return result