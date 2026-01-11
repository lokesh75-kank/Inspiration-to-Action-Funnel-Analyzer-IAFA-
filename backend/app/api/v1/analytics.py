"""Analytics endpoints with segment filtering support."""

from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from app.services.analytics_service import AnalyticsService
from app.services.genai_service import GenAIService

router = APIRouter()
analytics_service = AnalyticsService()
genai_service = GenAIService()


class StageMetrics(BaseModel):
    """Stage metrics model."""

    stage_name: str
    stage_order: int
    users: int
    conversion_rate: float
    drop_off_rate: float


class FunnelAnalyticsResponse(BaseModel):
    """Funnel analytics response model (supports segment breakdown)."""

    funnel_id: str
    funnel_name: str
    date_range: dict
    stages: Optional[List[StageMetrics]] = None
    overall_conversion_rate: Optional[float] = None
    total_users: Optional[int] = None
    completed_users: Optional[int] = None
    # Segment breakdown (optional)
    segment_by: Optional[str] = None
    segments: Optional[dict] = None
    total: Optional[dict] = None


@router.post("/funnel/{funnel_id}/recommendations")
async def get_funnel_recommendations(
    funnel_id: str,
    request_data: Dict = Body(...)
):
    """Get AI-powered insights and recommendations for a funnel."""
    try:
        org_id = request_data.get("org_id", "poc-org")
        start_date = request_data.get("start_date")
        end_date = request_data.get("end_date")
        segment_filters = request_data.get("segment_filters", {})
        segment_by = request_data.get("segment_by")
        audience = request_data.get("audience", "data_scientist")
        
        if not start_date or not end_date:
            raise HTTPException(status_code=400, detail="start_date and end_date are required")
        
        # Get analytics data first
        analytics_data = await analytics_service.calculate_funnel_metrics(
            funnel_id=funnel_id,
            org_id=org_id,
            start_date=start_date,
            end_date=end_date,
            user_intent=segment_filters.get("user_intent"),
            content_category=segment_filters.get("content_category"),
            surface=segment_filters.get("surface"),
            user_tenure=segment_filters.get("user_tenure"),
            segment_by=segment_by
        )
        
        if not analytics_data:
            raise HTTPException(status_code=404, detail="Funnel not found or no data available")
        
        # Generate recommendations using GenAI
        recommendations = await genai_service.generate_recommendations(
            funnel_id=funnel_id,
            analytics_data=analytics_data,
            start_date=start_date,
            end_date=end_date,
            filters=segment_filters,
            audience=audience
        )
        
        return recommendations
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")


@router.get("/funnel/{funnel_id}")
async def get_funnel_analytics(
    funnel_id: str,
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    # Segment filters (Phase 2)
    user_intent: Optional[str] = Query(None, description="Filter by user intent (comma-separated: Browser,Planner,Actor,Curator)"),
    content_category: Optional[str] = Query(None, description="Filter by content category (comma-separated)"),
    surface: Optional[str] = Query(None, description="Filter by surface (comma-separated: Home,Search,Boards,Profile)"),
    user_tenure: Optional[str] = Query(None, description="Filter by user tenure (comma-separated: New,Retained)"),
    # Segment breakdown
    segment_by: Optional[str] = Query(None, description="Break down by segment: user_intent, surface, user_tenure, content_category"),
):
    """Get funnel analytics for a date range with segment filtering support (POC: no auth required)."""
    service = AnalyticsService()
    try:
        # Validate date range
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        if end < start:
            raise HTTPException(
                status_code=400, detail="end_date must be after start_date"
            )
        if (end - start).days > 90:
            raise HTTPException(
                status_code=400, detail="Date range cannot exceed 90 days"
            )
        
        # Parse segment filters (comma-separated strings to lists)
        user_intent_list = [s.strip() for s in user_intent.split(",")] if user_intent else None
        content_category_list = [s.strip() for s in content_category.split(",")] if content_category else None
        surface_list = [s.strip() for s in surface.split(",")] if surface else None
        user_tenure_list = [s.strip() for s in user_tenure.split(",")] if user_tenure else None
        
        # Validate segment_by
        if segment_by and segment_by not in ["user_intent", "surface", "user_tenure", "content_category"]:
            raise HTTPException(
                status_code=400, 
                detail="segment_by must be one of: user_intent, surface, user_tenure, content_category"
            )

        analytics = await service.calculate_funnel_metrics(
            funnel_id=funnel_id,
            org_id="poc-org",
            start_date=start_date,
            end_date=end_date,
            user_intent=user_intent_list,
            content_category=content_category_list,
            surface=surface_list,
            user_tenure=user_tenure_list,
            segment_by=segment_by,
        )
        if not analytics:
            raise HTTPException(status_code=404, detail="Funnel not found")
        return analytics
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/funnel/{funnel_id}/report")
async def generate_ai_report(
    funnel_id: str,
    request_data: Dict = Body(...)
):
    """Generate AI-powered report for a funnel."""
    try:
        org_id = request_data.get("org_id", "poc-org")
        start_date = request_data.get("start_date")
        end_date = request_data.get("end_date")
        segment_filters = request_data.get("segment_filters", {})
        segment_by = request_data.get("segment_by")
        audience = request_data.get("audience", "data_scientist")
        format_type = request_data.get("format", "html")
        
        if not start_date or not end_date:
            raise HTTPException(status_code=400, detail="start_date and end_date are required")
        
        if format_type not in ["html", "markdown", "text"]:
            raise HTTPException(status_code=400, detail="format must be one of: html, markdown, text")
        
        if audience not in ["data_scientist", "executive", "product_manager"]:
            raise HTTPException(status_code=400, detail="audience must be one of: data_scientist, executive, product_manager")
        
        # Get analytics data first
        analytics_data = await analytics_service.calculate_funnel_metrics(
            funnel_id=funnel_id,
            org_id=org_id,
            start_date=start_date,
            end_date=end_date,
            user_intent=segment_filters.get("user_intent"),
            content_category=segment_filters.get("content_category"),
            surface=segment_filters.get("surface"),
            user_tenure=segment_filters.get("user_tenure"),
            segment_by=segment_by
        )
        
        if not analytics_data:
            raise HTTPException(status_code=404, detail="Funnel not found or no data available")
        
        # Generate AI report
        report = await genai_service.generate_report(
            funnel_id=funnel_id,
            analytics_data=analytics_data,
            start_date=start_date,
            end_date=end_date,
            filters=segment_filters,
            audience=audience,
            format=format_type
        )
        
        return report
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")
