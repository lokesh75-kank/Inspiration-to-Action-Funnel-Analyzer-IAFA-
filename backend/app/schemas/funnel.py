"""Funnel schemas."""

from pydantic import BaseModel
from typing import Optional, List


class FunnelStage(BaseModel):
    """Funnel stage schema."""

    order: int
    name: str
    event_type: str


class FunnelCreate(BaseModel):
    """Funnel creation schema."""

    project_id: str
    name: str
    description: Optional[str] = None
    stages: List[FunnelStage]


class FunnelResponse(BaseModel):
    """Funnel response schema."""

    id: str
    project_id: str
    name: str
    description: Optional[str]
    stages: List[dict]
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
