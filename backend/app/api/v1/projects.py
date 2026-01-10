"""Project management endpoints - POC Version (No Auth)."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from app.services.project_service import ProjectService

router = APIRouter()

# POC: Use a default project ID for local development
DEFAULT_PROJECT_ID = "poc-project-001"


class ProjectCreate(BaseModel):
    """Project creation request (Pinterest DS: product initiative, experiment scope, or surface-specific analysis)."""

    name: str
    domain: Optional[str] = Field(None, description="Product Surface / Environment (e.g., Home Feed, Search, Boards, Ads Manager)")


class ProjectResponse(BaseModel):
    """Project response model (Pinterest DS: product initiative or experiment scope)."""

    id: str
    name: str
    api_key: str
    domain: Optional[str] = Field(None, description="Product Surface / Environment (e.g., Home Feed, Search, Boards)")
    created_at: str
    updated_at: str


@router.get("", response_model=List[ProjectResponse])
async def list_projects():
    """List all projects (POC: single project)."""
    try:
        from app.storage.metadata_handler import MetadataHandler
        
        service = ProjectService()
        metadata_handler = MetadataHandler()
        
        # Check if default project exists first
        projects = metadata_handler.load_projects()
        existing_project = next((p for p in projects if p["id"] == DEFAULT_PROJECT_ID), None)
        
        if existing_project:
            # Project exists, return it (mask API key for security)
            project_dict = existing_project.copy()
            # Only mask if it's a full key (longer than 13 chars indicates full key)
            if len(project_dict.get("api_key", "")) > 13 and not project_dict["api_key"].endswith("***"):
                project_dict["api_key"] = project_dict["api_key"][:10] + "***"
            return [ProjectResponse(**project_dict)]
        else:
            # Create default Pinterest project (Pinterest DS: main product initiative)
            project = await service.create_project(
                org_id="poc-org",
                name="Pinterest",  # Can be renamed to specific initiative (e.g., "Home Feed Ranking Refresh", "Search Relevance Update")
                domain="Home Feed",  # Pinterest DS: Product Surface / Environment
                project_id=DEFAULT_PROJECT_ID
            )
            # Return with full API key visible on first creation
            return [ProjectResponse(**project)]
    except Exception as e:
        # Log error and return empty list with error message
        import traceback
        print(f"Error in list_projects: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to fetch projects: {str(e)}")


@router.post("", status_code=201, response_model=ProjectResponse)
async def create_project(project: ProjectCreate):
    """Create a new project (Pinterest DS: product initiative, experiment scope, or surface-specific analysis)."""
    service = ProjectService()
    try:
        new_project = await service.create_project(
            org_id="poc-org",
            name=project.name,
            domain=project.domain,  # Pinterest DS: Product Surface / Environment (e.g., Home Feed, Search, Boards)
        )
        return new_project
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """Get project details (POC: no auth check)."""
    service = ProjectService()
    project = await service.get_project(project_id, "poc-org")
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: str, project: ProjectCreate):
    """Update project settings (POC: no auth check)."""
    service = ProjectService()
    updated_project = await service.update_project(
        project_id=project_id,
        org_id="poc-org",
        name=project.name,
        domain=project.domain,
    )
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: str):
    """Delete a project (POC: no auth check)."""
    service = ProjectService()
    success = await service.delete_project(project_id, "poc-org")
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return None


@router.get("/{project_id}/tracking-code")
async def get_tracking_code(project_id: str):
    """Get JavaScript tracking code snippet (POC: no auth check)."""
    service = ProjectService()
    project = await service.get_project(project_id, "poc-org")
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    tracking_code = f"""
<script>
(function() {{
    const _iafa = window._iafa || [];
    const apiKey = '{project['api_key']}';
    const apiUrl = '{service.get_api_url()}';
    
    function track(eventType, properties = {{}}) {{
        const payload = {{
            event_type: eventType,
            user_id: _iafa.userId || getUserId(),
            session_id: _iafa.sessionId || getSessionId(),
            properties: properties,
            url: window.location.href,
            referrer: document.referrer,
            timestamp: new Date().toISOString()
        }};
        
        fetch(apiUrl + '/api/v1/track', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
                'X-API-Key': apiKey
            }},
            body: JSON.stringify(payload)
        }}).catch(console.error);
    }}
    
    function getUserId() {{
        let userId = localStorage.getItem('_iafa_user_id');
        if (!userId) {{
            userId = 'anon_' + Math.random().toString(36).substring(2, 15);
            localStorage.setItem('_iafa_user_id', userId);
        }}
        return userId;
    }}
    
    function getSessionId() {{
        let sessionId = sessionStorage.getItem('_iafa_session_id');
        if (!sessionId) {{
            sessionId = 'sess_' + Math.random().toString(36).substring(2, 15);
            sessionStorage.setItem('_iafa_session_id', sessionId);
        }}
        return sessionId;
    }}
    
    // Auto-track page views
    track('page_view');
    
    // Expose public API
    window._iafa = {{ track, userId: null, sessionId: null }};
}})();
</script>
"""
    return {
        "tracking_code": tracking_code.strip(),
        "api_key": project["api_key"][:10] + "***",  # Masked
        "instructions": "Copy and paste this code before </body> tag",
    }
