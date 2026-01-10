"""Project service."""

import uuid
import secrets
from datetime import datetime
from typing import Optional, List, Dict
from app.core.config import settings
from app.storage.metadata_handler import MetadataHandler


class ProjectService:
    """Service for project management."""

    def __init__(self):
        self.metadata_handler = MetadataHandler()
        self.api_url = f"http://{settings.API_HOST}:{settings.API_PORT}"

    def get_api_url(self) -> str:
        """Get API URL."""
        return self.api_url

    async def list_projects(self, org_id: str, include_full_api_key: bool = False) -> List[Dict]:
        """List all projects for an organization."""
        projects = self.metadata_handler.load_projects()
        org_projects = [p.copy() for p in projects if p["organization_id"] == org_id]
        # Mask API keys unless explicitly requested
        if not include_full_api_key:
            for project in org_projects:
                if "api_key" in project and len(project["api_key"]) > 13:
                    # Only mask if it's the full key (not already masked)
                    project["api_key"] = project["api_key"][:10] + "***"
        return org_projects

    async def create_project(
        self, org_id: str, name: str, domain: Optional[str] = None, project_id: Optional[str] = None
    ) -> Dict:
        """Create a new project."""
        # POC: Allow custom project_id for default project
        if project_id is None:
            project_id = str(uuid.uuid4())
        
        # Generate API key
        api_key = secrets.token_urlsafe(32)

        project = {
            "id": project_id,
            "organization_id": org_id,
            "name": name,
            "api_key": api_key,  # Store plain for first time, then hash
            "domain": domain,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        projects = self.metadata_handler.load_projects()
        # Check if project exists
        existing = next((p for p in projects if p["id"] == project_id), None)
        if existing:
            return existing
        projects.append(project)
        self.metadata_handler.save_projects(projects)

        # Create project directory structure
        self.metadata_handler.create_project_directory(project_id)

        # Return project with full API key (only on creation)
        return project
    
    async def get_project_by_id(self, project_id: str, include_full_api_key: bool = False) -> Optional[Dict]:
        """Get project by ID (POC: no org check)."""
        projects = self.metadata_handler.load_projects()
        project = next((p for p in projects if p["id"] == project_id), None)
        if project:
            project = project.copy()
            # Mask API key unless explicitly requested
            if not include_full_api_key and "api_key" in project and len(project["api_key"]) > 13:
                project["api_key"] = project["api_key"][:10] + "***"  # Mask
        return project

    async def get_project(self, project_id: str, org_id: str) -> Optional[Dict]:
        """Get project by ID."""
        projects = self.metadata_handler.load_projects()
        project = next(
            (
                p
                for p in projects
                if p["id"] == project_id and p["organization_id"] == org_id
            ),
            None,
        )
        if project and "api_key" in project:
            project["api_key"] = project["api_key"][:10] + "***"  # Mask
        return project

    async def get_project_by_api_key(self, api_key: str) -> Optional[Dict]:
        """Get project by API key (for tracking endpoints)."""
        projects = self.metadata_handler.load_projects()
        project = next((p for p in projects if p["api_key"] == api_key), None)
        return project

    async def update_project(
        self, project_id: str, org_id: str, name: str, domain: Optional[str] = None
    ) -> Optional[Dict]:
        """Update project settings."""
        projects = self.metadata_handler.load_projects()
        project = next(
            (
                p
                for p in projects
                if p["id"] == project_id and p["organization_id"] == org_id
            ),
            None,
        )
        if not project:
            return None

        project["name"] = name
        if domain:
            project["domain"] = domain
        project["updated_at"] = datetime.utcnow().isoformat()

        self.metadata_handler.save_projects(projects)

        # Mask API key
        project["api_key"] = project["api_key"][:10] + "***"
        return project

    async def delete_project(self, project_id: str, org_id: str) -> bool:
        """Delete a project."""
        projects = self.metadata_handler.load_projects()
        project = next(
            (
                p
                for p in projects
                if p["id"] == project_id and p["organization_id"] == org_id
            ),
            None,
        )
        if not project:
            return False

        projects.remove(project)
        self.metadata_handler.save_projects(projects)

        # TODO: Delete project directory and Parquet files
        return True
