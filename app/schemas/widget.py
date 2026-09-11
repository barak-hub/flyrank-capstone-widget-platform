from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WidgetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    widget_type: str = Field(default="membership", max_length=50)


class WidgetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    widget_type: str | None = Field(default=None, max_length=50)
    status: str | None = Field(default=None, max_length=30)


class WidgetResponse(BaseModel):
    id: int
    tenant_id: int
    name: str
    widget_type: str
    status: str
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
