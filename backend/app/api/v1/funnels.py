"""Funnel management endpoints - POC Version (No Auth)."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.services.funnel_service import FunnelService

router = APIRouter()

# POC: Default organization ID
DEFAULT_ORG_ID = "poc-org"


class FunnelStage(BaseModel):
    """Funnel stage definition."""

    order: int
    name: str
    event_type: str


class FunnelCreate(BaseModel):
    """Funnel creation request."""

    project_id: str
    name: str
    description: Optional[str] = None
    stages: List[FunnelStage]


class FunnelResponse(BaseModel):
    """Funnel response model."""

    id: str
    project_id: str
    name: str
    description: Optional[str]
    stages: List[dict]
    is_active: bool
    created_at: str
    updated_at: str


@router.get("", response_model=List[FunnelResponse])
async def list_funnels(project_id: Optional[str] = None):
    """List all funnels (POC: no auth required)."""
    service = FunnelService()
    funnels = await service.list_funnels(
        org_id=DEFAULT_ORG_ID, project_id=project_id
    )
    return funnels


@router.post("", status_code=201, response_model=FunnelResponse)
async def create_funnel(funnel: FunnelCreate):
    """Create a new funnel (POC: no auth required)."""
    service = FunnelService()
    try:
        new_funnel = await service.create_funnel(
            org_id=DEFAULT_ORG_ID,
            project_id=funnel.project_id,
            name=funnel.name,
            description=funnel.description,
            stages=[s.dict() for s in funnel.stages],
        )
        return new_funnel
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{funnel_id}", response_model=FunnelResponse)
async def get_funnel(funnel_id: str):
    """Get funnel details (POC: no auth required)."""
    service = FunnelService()
    funnel = await service.get_funnel(funnel_id, DEFAULT_ORG_ID)
    if not funnel:
        raise HTTPException(status_code=404, detail="Funnel not found")
    return funnel


@router.put("/{funnel_id}", response_model=FunnelResponse)
async def update_funnel(funnel_id: str, funnel: FunnelCreate):
    """Update funnel definition (POC: no auth required)."""
    service = FunnelService()
    updated_funnel = await service.update_funnel(
        funnel_id=funnel_id,
        org_id=DEFAULT_ORG_ID,
        name=funnel.name,
        description=funnel.description,
        stages=[s.dict() for s in funnel.stages],
    )
    if not updated_funnel:
        raise HTTPException(status_code=404, detail="Funnel not found")
    return updated_funnel


@router.delete("/{funnel_id}", status_code=204)
async def delete_funnel(funnel_id: str):
    """Delete a funnel (POC: no auth required)."""
    service = FunnelService()
    success = await service.delete_funnel(funnel_id, DEFAULT_ORG_ID)
    if not success:
        raise HTTPException(status_code=404, detail="Funnel not found")
    return None
