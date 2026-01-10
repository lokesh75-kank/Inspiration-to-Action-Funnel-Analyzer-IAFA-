"""Funnel service."""

import uuid
from datetime import datetime
from typing import Optional, List, Dict
from app.storage.metadata_handler import MetadataHandler


class FunnelService:
    """Service for funnel management."""

    def __init__(self):
        self.metadata_handler = MetadataHandler()

    async def list_funnels(
        self, org_id: str, project_id: Optional[str] = None
    ) -> List[Dict]:
        """List all funnels for an organization."""
        funnels = self.metadata_handler.load_funnels()
        org_funnels = [f for f in funnels if f["organization_id"] == org_id]
        if project_id:
            org_funnels = [f for f in org_funnels if f["project_id"] == project_id]
        return org_funnels

    async def create_funnel(
        self,
        org_id: str,
        project_id: str,
        name: str,
        description: Optional[str],
        stages: List[Dict],
    ) -> Dict:
        """Create a new funnel."""
        # Validate stages
        if len(stages) > 5:
            raise ValueError("Maximum 5 stages allowed in MVP")
        if not stages:
            raise ValueError("At least one stage is required")

        # Validate stage orders
        orders = [s["order"] for s in stages]
        if sorted(orders) != list(range(1, len(stages) + 1)):
            raise ValueError("Stage orders must be sequential (1, 2, 3, ...)")

        funnel_id = str(uuid.uuid4())
        funnel = {
            "id": funnel_id,
            "project_id": project_id,
            "organization_id": org_id,
            "name": name,
            "description": description,
            "stages": stages,
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        funnels = self.metadata_handler.load_funnels()
        funnels.append(funnel)
        self.metadata_handler.save_funnels(funnels)

        return funnel

    async def get_funnel(self, funnel_id: str, org_id: str) -> Optional[Dict]:
        """Get funnel by ID."""
        funnels = self.metadata_handler.load_funnels()
        funnel = next(
            (
                f
                for f in funnels
                if f["id"] == funnel_id and f["organization_id"] == org_id
            ),
            None,
        )
        return funnel

    async def update_funnel(
        self,
        funnel_id: str,
        org_id: str,
        name: str,
        description: Optional[str],
        stages: List[Dict],
    ) -> Optional[Dict]:
        """Update funnel definition."""
        funnels = self.metadata_handler.load_funnels()
        funnel = next(
            (
                f
                for f in funnels
                if f["id"] == funnel_id and f["organization_id"] == org_id
            ),
            None,
        )
        if not funnel:
            return None

        # Validate stages
        if len(stages) > 5:
            raise ValueError("Maximum 5 stages allowed in MVP")

        funnel["name"] = name
        funnel["description"] = description
        funnel["stages"] = stages
        funnel["updated_at"] = datetime.utcnow().isoformat()

        self.metadata_handler.save_funnels(funnels)
        return funnel

    async def delete_funnel(self, funnel_id: str, org_id: str) -> bool:
        """Delete a funnel."""
        funnels = self.metadata_handler.load_funnels()
        funnel = next(
            (
                f
                for f in funnels
                if f["id"] == funnel_id and f["organization_id"] == org_id
            ),
            None,
        )
        if not funnel:
            return False

        funnels.remove(funnel)
        self.metadata_handler.save_funnels(funnels)
        return True
