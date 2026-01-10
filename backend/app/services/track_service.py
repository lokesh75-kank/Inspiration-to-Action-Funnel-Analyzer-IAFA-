"""Event tracking service."""

import uuid
from datetime import datetime
from typing import Dict, List
from app.storage.parquet_handler import ParquetHandler
from app.core.config import settings


class TrackService:
    """Service for event tracking."""

    def __init__(self):
        self.parquet_handler = ParquetHandler()
        self.event_buffer = {}  # project_id -> list of events
        self.buffer_size = settings.EVENT_BUFFER_SIZE

    async def track_event(
        self,
        project_id: str,
        event_type: str,
        user_id: str,
        session_id: str = None,
        properties: Dict = None,
        url: str = None,
        referrer: str = None,
        user_agent: str = None,
        timestamp: str = None,
        # Segment dimensions (Phase 2)
        user_intent: str = None,
        content_category: str = None,
        surface: str = None,
        user_tenure: str = None,
        # Experiment tracking (Phase 3 - structure ready)
        experiment_id: str = None,
        variant: str = None,
    ) -> str:
        """Track a single event with segmentation support."""
        event_id = str(uuid.uuid4())
        event = {
            "id": event_id,
            "project_id": project_id,
            "event_type": event_type,
            "user_id": user_id,
            "session_id": session_id,
            "properties": properties or {},
            "url": url,
            "referrer": referrer,
            "user_agent": user_agent,
            "ip_address": None,  # TODO: Get from request
            "created_at": timestamp or datetime.utcnow().isoformat(),
            # Segment dimensions (Phase 2)
            "user_intent": user_intent or "Unknown",
            "content_category": content_category or None,
            "surface": surface or "Unknown",
            "user_tenure": user_tenure or "Unknown",
            # Experiment tracking (Phase 3)
            "experiment_id": experiment_id or None,
            "variant": variant or None,
        }

        # Add to buffer
        if project_id not in self.event_buffer:
            self.event_buffer[project_id] = []
        self.event_buffer[project_id].append(event)

        # Flush if buffer is full
        if len(self.event_buffer[project_id]) >= self.buffer_size:
            await self._flush_buffer(project_id)

        return event_id

    async def track_batch_events(self, project_id: str, events: List[Dict]) -> List[str]:
        """Track multiple events with segmentation support."""
        event_ids = []
        for event_data in events:
            event_id = await self.track_event(
                project_id=project_id,
                event_type=event_data["event_type"],
                user_id=event_data["user_id"],
                session_id=event_data.get("session_id"),
                properties=event_data.get("properties", {}),
                url=event_data.get("url"),
                referrer=event_data.get("referrer"),
                user_agent=event_data.get("user_agent"),
                timestamp=event_data.get("timestamp"),
                # Segment dimensions (Phase 2)
                user_intent=event_data.get("user_intent"),
                content_category=event_data.get("content_category"),
                surface=event_data.get("surface"),
                user_tenure=event_data.get("user_tenure"),
                # Experiment tracking (Phase 3)
                experiment_id=event_data.get("experiment_id"),
                variant=event_data.get("variant"),
            )
            event_ids.append(event_id)

        # Flush buffer for this project
        if project_id in self.event_buffer:
            await self._flush_buffer(project_id)

        return event_ids

    async def _flush_buffer(self, project_id: str):
        """Flush events from buffer to Parquet file."""
        if project_id not in self.event_buffer:
            return

        events = self.event_buffer[project_id]
        if not events:
            return

        # Write to Parquet
        await self.parquet_handler.append_events(project_id, events)

        # Clear buffer
        self.event_buffer[project_id] = []
