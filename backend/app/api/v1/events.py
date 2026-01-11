"""Event metadata endpoints - get available event types."""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.storage.duckdb_query import DuckDBQuery
from app.services.project_service import ProjectService

router = APIRouter()


@router.get("/types", response_model=List[str])
async def get_event_types(
    project_id: str = Query(..., description="Project ID"),
):
    """Get list of available event types in the project's data."""
    try:
        service = ProjectService()
        project = await service.get_project_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        query_handler = DuckDBQuery()
        
        # Get list of event types from Parquet files
        event_types = query_handler.get_available_event_types(project_id)
        
        return event_types
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get event types: {str(e)}")
