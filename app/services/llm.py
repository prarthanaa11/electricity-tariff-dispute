from typing import Any, Protocol


class ModelProvider(Protocol):
    def generate(
        self,
        prompt: str,
    ) -> dict[str, Any]:
        ...


class StubModelProvider:
    """
    Deterministic provider for development and testing.

    It does not make legal determinations.
    """

    def generate(
        self,
        prompt: str,
    ) -> dict[str, Any]:
        return {
            "provider": "stub",
            "response": (
                "Insufficient evidence for a "
                "regulatory determination."
            ),
            "needs_more_evidence": True,
            "tool_calls": [],
        }


def get_model_provider() -> ModelProvider:
    return StubModelProvider()