from pydantic import BaseModel, EmailStr, Field, model_validator


class SubmissionCreate(BaseModel):
    request_type: str = Field(min_length=1, max_length=30)
    visitor_name: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=50)
    membership_id: str | None = Field(default=None, max_length=100)
    room_number: str | None = Field(default=None, max_length=50)
    message: str | None = Field(default=None, max_length=5000)
    honeypot: str | None = Field(default=None, max_length=100)

    @model_validator(mode="after")
    def validate_contact_details(self):
        if not self.email and not self.phone:
            raise ValueError("Either email or phone is required")
        return self
