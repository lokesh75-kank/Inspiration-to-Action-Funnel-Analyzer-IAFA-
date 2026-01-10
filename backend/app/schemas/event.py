"""Event schemas."""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Literal
from datetime import datetime


# User intent segments (Pinterest DS specific)
UserIntentSegment = Literal["Browser", "Planner", "Actor", "Curator", "Unknown"]
UserTenure = Literal["New", "Retained", "Unknown"]
Surface = Literal["Home", "Search", "Boards", "Profile", "Other", "Unknown"]


class EventSchema(BaseModel):
    """Event tracking schema with segmentation support."""

    event_type: str = Field(..., min_length=1, max_length=100)
    user_id: str = Field(..., min_length=1, max_length=255)
    session_id: Optional[str] = None
    properties: Optional[Dict] = Field(default_factory=dict)
    url: Optional[str] = Field(None, max_length=500)
    referrer: Optional[str] = Field(None, max_length=500)
    user_agent: Optional[str] = None
    timestamp: Optional[str] = None  # ISO format
    
    # Segment dimensions (Pinterest DS specific)
    user_intent: Optional[UserIntentSegment] = Field(None, description="User intent segment: Browser, Planner, Actor, Curator")
    content_category: Optional[str] = Field(None, max_length=100, description="Content category (e.g., home_decor, recipes, travel)")
    surface: Optional[Surface] = Field(None, description="Surface where event occurred: Home, Search, Boards, Profile")
    user_tenure: Optional[UserTenure] = Field(None, description="User tenure: New, Retained")
    
    # Experiment tracking (for Phase 3, but adding structure now)
    experiment_id: Optional[str] = Field(None, max_length=100, description="Experiment ID if part of an experiment")
    variant: Optional[str] = Field(None, max_length=50, description="Experiment variant: control, treatment, etc.")

    @validator("properties")
    def validate_properties(cls, v):
        """Ensure properties is a dictionary."""
        if not isinstance(v, dict):
            raise ValueError("Properties must be a dictionary")
        return v
    
    @validator("user_intent")
    def validate_user_intent(cls, v):
        """Validate user intent segment."""
        if v and v not in ["Browser", "Planner", "Actor", "Curator", "Unknown"]:
            raise ValueError("user_intent must be one of: Browser, Planner, Actor, Curator, Unknown")
        return v or "Unknown"
    
    @validator("surface")
    def validate_surface(cls, v):
        """Validate surface."""
        if v and v not in ["Home", "Search", "Boards", "Profile", "Other", "Unknown"]:
            raise ValueError("surface must be one of: Home, Search, Boards, Profile, Other, Unknown")
        return v or "Unknown"
    
    @validator("user_tenure")
    def validate_user_tenure(cls, v):
        """Validate user tenure."""
        if v and v not in ["New", "Retained", "Unknown"]:
            raise ValueError("user_tenure must be one of: New, Retained, Unknown")
        return v or "Unknown"


class BatchEventSchema(BaseModel):
    """Batch event tracking schema."""

    events: list[EventSchema]
