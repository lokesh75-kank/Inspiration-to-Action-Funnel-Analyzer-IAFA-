"""Background tasks for periodic operations."""

import asyncio
from app.core.config import settings


class BackgroundTaskManager:
    """Manager for background tasks."""

    def __init__(self):
        self._flush_task = None
        self._running = False

    async def start_periodic_flush(self):
        """Start periodic event buffer flush."""
        from app.services.track_service import TrackService
        track_service = TrackService()
        
        self._running = True
        while self._running:
            await asyncio.sleep(settings.EVENT_FLUSH_INTERVAL)
            # Flush all project buffers
            for project_id in list(track_service.event_buffer.keys()):
                if track_service.event_buffer[project_id]:
                    await track_service._flush_buffer(project_id)

    def start(self):
        """Start background tasks."""
        if self._flush_task is None or self._flush_task.done():
            self._flush_task = asyncio.create_task(self.start_periodic_flush())

    def stop(self):
        """Stop background tasks."""
        self._running = False
        if self._flush_task and not self._flush_task.done():
            self._flush_task.cancel()


# Global instance
background_manager = BackgroundTaskManager()
