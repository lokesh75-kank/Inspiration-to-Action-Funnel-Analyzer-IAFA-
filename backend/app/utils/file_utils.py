"""File utility functions."""

from pathlib import Path
from typing import List
from datetime import datetime, timedelta
from app.core.config import settings


def generate_parquet_file_paths(
    project_id: str, start_date: str, end_date: str
) -> List[Path]:
    """Generate list of Parquet file paths for date range."""
    data_dir = Path(settings.DATA_DIR)
    events_dir = data_dir / "events"
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    files = []
    current = start

    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        file_path = (
            events_dir
            / f"project_{project_id}"
            / str(current.year)
            / f"{current.month:02d}"
            / f"events_{date_str}.parquet"
        )

        if file_path.exists():
            files.append(file_path)

        current += timedelta(days=1)

    return files
