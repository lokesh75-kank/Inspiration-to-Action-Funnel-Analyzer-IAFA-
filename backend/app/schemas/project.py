"""Project schemas."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectCreate(BaseModel):
    """Project creation schema."""

    name: str
    domain: Optional[str] = None


class ProjectResponse(BaseModel):
    """Project response schema."""

    id: str
    name: str
    api_key: str
    domain: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
