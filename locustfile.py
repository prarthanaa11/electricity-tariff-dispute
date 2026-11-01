import time

from locust import HttpUser, task, between


class TariffUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def health_check(self):
        self.client.get(
            "/health",
            name="health",
        )

    @task
    def submit_dispute(self):
        payload = {
            "consumer_reference": "LOAD-TEST-001",
            "complaint_text": (
                "My domestic connection is used "
                "partly for a tailoring shop."
            ),
            "premises_type": "mixed_use",
            "connected_load_kw": 3.0,
            "current_tariff_category": "domestic",
        }

        response = self.client.post(
            "/api/v1/disputes",
            json=payload,
            name="submit_dispute",
        )

        if response.status_code != 200:
            return

        run_id = response.json().get("run_id")

        if not run_id:
            return

        started = time.perf_counter()
        deadline = started + 120

        while time.perf_counter() < deadline:
            status_response = self.client.get(
                f"/api/v1/disputes/{run_id}",
                name="poll_dispute",
            )

            if status_response.status_code != 200:
                time.sleep(1)
                continue

            state = status_response.json().get(
                "status"
            )

            if state in {
                "completed",
                "escalated",
                "failed",
            }:
                elapsed = time.perf_counter() - started

                # This elapsed value is measured locally.
                # Record it in the benchmark results using
                # a custom Locust event or a separate runner.
                print(
                    f"Run {run_id} finished "
                    f"with state={state}, "
                    f"elapsed={elapsed:.2f}s"
                )

                break

            time.sleep(1)