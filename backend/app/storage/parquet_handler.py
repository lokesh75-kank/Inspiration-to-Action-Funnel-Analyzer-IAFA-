"""Parquet file handler for event storage."""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from app.core.config import settings


class ParquetHandler:
    """Handler for Parquet file operations."""

    def __init__(self):
        self.data_dir = Path(settings.DATA_DIR)
        self.events_dir = self.data_dir / "events"
        self.events_dir.mkdir(parents=True, exist_ok=True)

    def _get_parquet_file_path(self, project_id: str, date: datetime) -> Path:
        """Get Parquet file path for a project and date."""
        year = date.year
        month = date.month
        date_str = date.strftime("%Y-%m-%d")
        project_dir = self.events_dir / f"project_{project_id}" / str(year) / f"{month:02d}"
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir / f"events_{date_str}.parquet"

    async def append_events(self, project_id: str, events: List[Dict]):
        """Append events to Parquet file (batch write)."""
        if not events:
            return

        # Use asyncio to run blocking operations in thread pool
        import asyncio
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._write_events_sync, project_id, events)

    def _write_events_sync(self, project_id: str, events: List[Dict]):
        """Synchronously write events to Parquet (run in executor)."""
        # Group events by date
        events_by_date = {}
        for event in events:
            try:
                event_date = datetime.fromisoformat(event["created_at"].replace("Z", "+00:00"))
            except:
                event_date = datetime.utcnow()
            date_key = event_date.date()
            if date_key not in events_by_date:
                events_by_date[date_key] = []
            events_by_date[date_key].append(event)

        # Write events to respective date files
        for date_key, date_events in events_by_date.items():
            file_path = self._get_parquet_file_path(
                project_id, datetime.combine(date_key, datetime.min.time())
            )

            # Convert to DataFrame
            df = pd.DataFrame(date_events)

            # Convert properties to JSON string
            df["properties"] = df["properties"].apply(lambda x: json.dumps(x) if isinstance(x, dict) else "{}")
            df["created_at"] = pd.to_datetime(df["created_at"], utc=True, errors="coerce")
            df["created_at"] = df["created_at"].fillna(pd.Timestamp.now(tz="UTC"))

            # Ensure all required columns exist
            required_cols = [
                "id", "project_id", "event_type", "user_id", "session_id", "properties", 
                "url", "referrer", "user_agent", "ip_address",
                # Segment dimensions (Phase 2)
                "user_intent", "content_category", "surface", "user_tenure",
                # Experiment tracking (Phase 3)
                "experiment_id", "variant"
            ]
            for col in required_cols:
                if col not in df.columns:
                    df[col] = None

            # Fill missing values with appropriate defaults
            df = df.fillna({
                "user_intent": "Unknown",
                "surface": "Unknown",
                "user_tenure": "Unknown",
                "content_category": None,
                "experiment_id": None,
                "variant": None,
            })
            df = df.fillna("")  # Fill remaining None values

            # Write to Parquet (append if file exists)
            if file_path.exists():
                try:
                    # Read existing data
                    existing_df = pd.read_parquet(file_path)
                    # Append new events
                    combined_df = pd.concat([existing_df, df], ignore_index=True)
                    # Write back
                    combined_df.to_parquet(file_path, compression="snappy", index=False)
                except Exception as e:
                    # If read fails, just write new file
                    df.to_parquet(file_path, compression="snappy", index=False)
            else:
                # Create new file
                df.to_parquet(file_path, compression="snappy", index=False)
