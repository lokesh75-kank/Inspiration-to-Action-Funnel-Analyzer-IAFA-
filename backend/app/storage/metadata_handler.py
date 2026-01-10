"""Metadata handler for JSON file operations."""

import json
import os
import uuid
from pathlib import Path
from typing import List, Dict
from app.core.config import settings
import aiofiles
import asyncio


class MetadataHandler:
    """Handler for metadata JSON files."""

    def __init__(self):
        self.data_dir = Path(settings.DATA_DIR)
        self.metadata_dir = self.data_dir / "metadata"
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

        # Initialize metadata files if they don't exist
        self._init_metadata_files()

    def _init_metadata_files(self):
        """Initialize metadata files if they don't exist."""
        users_file = self.metadata_dir / "users.json"
        projects_file = self.metadata_dir / "projects.json"
        funnels_file = self.metadata_dir / "funnels.json"
        orgs_file = self.metadata_dir / "organizations.json"

        if not users_file.exists():
            self._save_json_sync(users_file, {"users": []})
        if not projects_file.exists():
            self._save_json_sync(projects_file, {"projects": []})
        if not funnels_file.exists():
            self._save_json_sync(funnels_file, {"funnels": []})
        if not orgs_file.exists():
            self._save_json_sync(orgs_file, {"organizations": []})

    def _save_json_sync(self, file_path: Path, data: Dict):
        """Synchronously save JSON file (for initialization only)."""
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    async def _load_json(self, file_path: Path) -> Dict:
        """Asynchronously load JSON file."""
        if not file_path.exists():
            return {}
        async with aiofiles.open(file_path, "r") as f:
            content = await f.read()
            return json.loads(content) if content else {}

    async def _save_json(self, file_path: Path, data: Dict):
        """Asynchronously save JSON file (atomic write)."""
        # Write to temp file first
        temp_file = file_path.with_suffix(".tmp")
        async with aiofiles.open(temp_file, "w") as f:
            await f.write(json.dumps(data, indent=2))
        # Atomic rename
        os.replace(temp_file, file_path)

    def load_users(self) -> List[Dict]:
        """Load users from JSON file (synchronous for now)."""
        users_file = self.metadata_dir / "users.json"
        if not users_file.exists():
            return []
        with open(users_file, "r") as f:
            data = json.load(f)
            return data.get("users", [])

    def save_users(self, users: List[Dict]):
        """Save users to JSON file (synchronous wrapper)."""
        users_file = self.metadata_dir / "users.json"
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                self._save_json_sync(users_file, {"users": users})
            else:
                asyncio.run(self._save_json(users_file, {"users": users}))
        except RuntimeError:
            self._save_json_sync(users_file, {"users": users})

    def load_projects(self) -> List[Dict]:
        """Load projects from JSON file."""
        projects_file = self.metadata_dir / "projects.json"
        if not projects_file.exists():
            return []
        with open(projects_file, "r") as f:
            data = json.load(f)
            return data.get("projects", [])

    def save_projects(self, projects: List[Dict]):
        """Save projects to JSON file (synchronous wrapper)."""
        projects_file = self.metadata_dir / "projects.json"
        try:
            # Try to use existing event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is running, use synchronous save
                self._save_json_sync(projects_file, {"projects": projects})
            else:
                # If no loop running, create one
                asyncio.run(self._save_json(projects_file, {"projects": projects}))
        except RuntimeError:
            # No event loop, use synchronous save
            self._save_json_sync(projects_file, {"projects": projects})

    def load_funnels(self) -> List[Dict]:
        """Load funnels from JSON file."""
        funnels_file = self.metadata_dir / "funnels.json"
        if not funnels_file.exists():
            return []
        with open(funnels_file, "r") as f:
            data = json.load(f)
            return data.get("funnels", [])

    def save_funnels(self, funnels: List[Dict]):
        """Save funnels to JSON file (synchronous wrapper)."""
        funnels_file = self.metadata_dir / "funnels.json"
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                self._save_json_sync(funnels_file, {"funnels": funnels})
            else:
                asyncio.run(self._save_json(funnels_file, {"funnels": funnels}))
        except RuntimeError:
            self._save_json_sync(funnels_file, {"funnels": funnels})

    def load_organizations(self) -> List[Dict]:
        """Load organizations from JSON file."""
        orgs_file = self.metadata_dir / "organizations.json"
        if not orgs_file.exists():
            return []
        with open(orgs_file, "r") as f:
            data = json.load(f)
            return data.get("organizations", [])

    def save_organizations(self, orgs: List[Dict]):
        """Save organizations to JSON file (synchronous wrapper)."""
        orgs_file = self.metadata_dir / "organizations.json"
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                self._save_json_sync(orgs_file, {"organizations": orgs})
            else:
                asyncio.run(self._save_json(orgs_file, {"organizations": orgs}))
        except RuntimeError:
            self._save_json_sync(orgs_file, {"organizations": orgs})

    def create_project_directory(self, project_id: str):
        """Create directory structure for a project."""
        project_dir = self.data_dir / "events" / f"project_{project_id}"
        project_dir.mkdir(parents=True, exist_ok=True)
