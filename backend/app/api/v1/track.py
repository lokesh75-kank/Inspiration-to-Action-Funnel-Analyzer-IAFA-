"""Event tracking endpoints (public API)."""

from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime
from app.services.track_service import TrackService
from app.services.project_service import ProjectService

router = APIRouter()


class EventSchema(BaseModel):
    """Event tracking schema with segmentation support."""

    event_type: str
    user_id: str
    session_id: Optional[str] = None
    properties: Optional[Dict] = {}
    url: Optional[str] = None
    referrer: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: Optional[str] = None  # ISO format
    
    # Segment dimensions (Phase 2)
    user_intent: Optional[str] = None  # Browser, Planner, Actor, Curator
    content_category: Optional[str] = None
    surface: Optional[str] = None  # Home, Search, Boards, Profile
    user_tenure: Optional[str] = None  # New, Retained
    
    # Experiment tracking (Phase 3)
    experiment_id: Optional[str] = None
    variant: Optional[str] = None


class BatchEventSchema(BaseModel):
    """Batch event tracking schema."""

    events: List[EventSchema]


async def verify_api_key(x_api_key: str = Header(None)) -> str:
    """Verify API key and return project ID (POC: optional, uses default if missing)."""
    # POC: If no API key provided, use default project
    if not x_api_key:
        return "poc-project-001"
    
    project_service = ProjectService()
    project = await project_service.get_project_by_api_key(x_api_key)
    if not project:
        # POC: If API key invalid, still use default project for demonstration
        return "poc-project-001"
    return project["id"]


@router.post("")
async def track_event(
    event: EventSchema, 
    x_api_key: str = Header(None),
    project_id: str = Depends(verify_api_key)
):
    """Track a single event."""
    track_service = TrackService()
    try:
        event_id = await track_service.track_event(
            project_id=project_id,
            event_type=event.event_type,
            user_id=event.user_id,
            session_id=event.session_id,
            properties=event.properties,
            url=event.url,
            referrer=event.referrer,
            user_agent=event.user_agent,
            timestamp=event.timestamp or datetime.utcnow().isoformat(),
            # Segment dimensions (Phase 2)
            user_intent=event.user_intent,
            content_category=event.content_category,
            surface=event.surface,
            user_tenure=event.user_tenure,
            # Experiment tracking (Phase 3)
            experiment_id=event.experiment_id,
            variant=event.variant,
        )
        return {"success": True, "event_id": event_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/batch")
async def track_batch_events(
    batch: BatchEventSchema,
    x_api_key: str = Header(None),
    project_id: str = Depends(verify_api_key)
):
    """Track multiple events in a single request."""
    track_service = TrackService()
    try:
        event_ids = await track_service.track_batch_events(
            project_id=project_id, events=[e.dict() for e in batch.events]
        )
        return {
            "success": True,
            "events_processed": len(event_ids),
            "event_ids": event_ids,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
