from enum import Enum

from pydantic import BaseModel, Field, model_validator


class ComplaintType(str, Enum):
    TARIFF_CATEGORY = "tariff_category"
    METER_ACCURACY = "meter_accuracy"
    LOAD_VIOLATION = "load_violation"
    ARREARS = "arrears"
    DISCONNECTION = "disconnection"


class PremisesType(str, Enum):
    DOMESTIC = "domestic"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    MIXED_USE = "mixed_use"
    OTHER = "other"


class DisputeRequest(BaseModel):
    consumer_reference: str = Field(
        min_length=1,
        max_length=64,
    )

    complaint_text: str = Field(
        min_length=10,
        max_length=5000,
    )

    premises_type: PremisesType

    connected_load_kw: float = Field(
        gt=0,
        le=10000,
    )

    current_tariff_category: str = Field(
        min_length=1,
        max_length=100,
    )

    complaint_type: ComplaintType | None = None

    @model_validator(mode="after")
    def validate_cross_fields(self):
        if (
            self.premises_type == PremisesType.MIXED_USE
            and not self.complaint_text.strip()
        ):
            raise ValueError(
                "Mixed-use premises require complaint details."
            )

        return self