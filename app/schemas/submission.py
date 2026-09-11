from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class SubmissionCreate(BaseModel):
    request_type: str = Field(
        min_length=1,
        max_length=30,
    )
    visitor_name: str | None = Field(
        default=None,
        max_length=150,
    )
    email: EmailStr | None = None
    phone: str | None = Field(
        default=None,
        max_length=50,
    )
    membership_id: str | None = Field(
        default=None,
        max_length=100,
    )
    room_number: str | None = Field(
        default=None,
        max_length=50,
    )
    message: str | None = Field(
        default=None,
        max_length=2000,
    )
    website: str | None = Field(
        default=None,
        max_length=200,
    )

    @model_validator(mode="after")
    def validate_submission(self):
        allowed_types = {
            "membership",
            "general",
            "hotel_guest",
        }

        if self.request_type not in allowed_types:
            raise ValueError(
                "request_type must be membership, general, or hotel_guest"
            )

        if not self.email and not self.phone:
            raise ValueError("At least an email or phone number is required")

        if self.request_type == "hotel_guest" and not self.room_number:
            raise ValueError(
                "room_number is required for hotel_guest requests"
            )

        return self


class SubmissionResponse(BaseModel):
    id: int
    tenant_id: int
    widget_id: int
    request_type: str
    visitor_name: str | None
    email: str | None
    phone: str | None
    membership_id: str | None
    room_number: str | None
    message: str | None
    geo_country: str | None

    model_config = ConfigDict(from_attributes=True)
