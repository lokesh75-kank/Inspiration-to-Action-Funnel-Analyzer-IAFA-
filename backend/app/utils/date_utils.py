"""Date utility functions for partitioning and date range operations."""

from datetime import datetime, timedelta
from typing import List, Tuple
from pathlib import Path
from app.core.config import settings


def get_date_range(start_date: str, end_date: str) -> Tuple[datetime, datetime]:
    """Parse date strings and return datetime objects."""
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    return start, end


def generate_date_list(start_date: str, end_date: str) -> List[datetime]:
    """Generate list of dates between start and end (inclusive)."""
    start, end = get_date_range(start_date, end_date)
    dates = []
    current = start
    while current <= end:
        dates.append(current)
        current += timedelta(days=1)
    return dates


def get_parquet_directory_path(project_id: str, date: datetime) -> Path:
    """Get directory path for a project and date."""
    data_dir = Path(settings.DATA_DIR)
    year = date.year
    month = date.month
    return data_dir / "events" / f"project_{project_id}" / str(year) / f"{month:02d}"


def get_parquet_file_path(project_id: str, date: datetime) -> Path:
    """Get Parquet file path for a project and date."""
    directory = get_parquet_directory_path(project_id, date)
    date_str = date.strftime("%Y-%m-%d")
    return directory / f"events_{date_str}.parquet"


def format_date_for_query(date: datetime) -> str:
    """Format datetime for DuckDB query."""
    return date.strftime("%Y-%m-%d")


def validate_date_range(start_date: str, end_date: str, max_days: int = 90) -> None:
    """Validate date range."""
    start, end = get_date_range(start_date, end_date)
    if end < start:
        raise ValueError("end_date must be after start_date")
    if (end - start).days > max_days:
        raise ValueError(f"Date range cannot exceed {max_days} days")
