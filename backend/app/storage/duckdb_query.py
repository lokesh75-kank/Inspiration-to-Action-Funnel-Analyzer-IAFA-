"""DuckDB query handler for analytics."""

import duckdb
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
from app.core.config import settings


class DuckDBQuery:
    """Handler for DuckDB queries on Parquet files."""

    def __init__(self):
        self.data_dir = Path(settings.DATA_DIR)
        self.events_dir = self.data_dir / "events"
        self.conn = duckdb.connect()

    def _generate_parquet_file_paths(
        self, project_id: str, start_date: str, end_date: str
    ) -> List[str]:
        """Generate list of Parquet file paths for date range."""
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)

        files = []
        current = start

        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            file_path = (
                self.events_dir
                / f"project_{project_id}"
                / str(current.year)
                / f"{current.month:02d}"
                / f"events_{date_str}.parquet"
            )

            if file_path.exists():
                files.append(str(file_path.absolute()))

            current += timedelta(days=1)

        return files

    def get_available_event_types(self, project_id: str) -> List[str]:
        """Get list of distinct event types from all Parquet files for a project."""
        try:
            # Get all Parquet files in the events directory recursively
            events_dir = self.events_dir / f"project_{project_id}"
            if not events_dir.exists():
                return []
            
            # Find all Parquet files recursively (year/month subdirectories)
            parquet_files = list(events_dir.rglob("*.parquet"))
            if not parquet_files:
                return []
            
            # Build file list string for DuckDB
            files_list = [f"'{str(f.absolute())}'" for f in parquet_files]
            files_str = f"[{', '.join(files_list)}]"
            
            # Query distinct event types
            query = f"""
            SELECT DISTINCT event_type
            FROM read_parquet({files_str})
            ORDER BY event_type
            """
            
            result = self.conn.execute(query).fetchall()
            return [row[0] for row in result]
            
        except Exception as e:
            print(f"Error getting event types: {e}")
            return []

    def calculate_funnel_metrics(
        self,
        funnel_id: str,
        project_id: str,
        stages: List[Dict],
        start_date: str,
        end_date: str,
        # Segment filters (Phase 2)
        user_intent: List[str] = None,
        content_category: List[str] = None,
        surface: List[str] = None,
        user_tenure: List[str] = None,
        # Segment breakdown (if None, aggregate; if specified, break down by segment)
        segment_by: str = None,  # "user_intent", "surface", "user_tenure", "content_category"
    ) -> Dict:
        """Calculate funnel metrics using DuckDB with segment filtering support."""
        # Generate Parquet file paths
        parquet_files = self._generate_parquet_file_paths(
            project_id, start_date, end_date
        )

        if not parquet_files:
            # Return empty metrics
            empty_result = {stage["name"]: 0 for stage in stages}
            if segment_by:
                return {"segments": {}, "total": empty_result}
            return empty_result

        # Build file paths list for DuckDB (proper syntax)
        files_list = [f"'{f}'" for f in parquet_files]
        files_str = f"[{', '.join(files_list)}]"

        # Get event types from stages
        event_types = [stage["event_type"] for stage in stages]
        event_types_str = "', '".join(event_types)

        # Build WHERE clause with segment filters
        where_conditions = [
            f"event_type IN ('{event_types_str}')",
            f"CAST(created_at AS DATE) >= CAST('{start_date}' AS DATE)",
            f"CAST(created_at AS DATE) <= CAST('{end_date}' AS DATE)"
        ]
        
        # Add segment filters (with null/Unknown handling for backward compatibility)
        if user_intent:
            intent_list = "', '".join(user_intent)
            where_conditions.append(f"(COALESCE(user_intent, 'Unknown') IN ('{intent_list}') OR user_intent IN ('{intent_list}'))")
        if content_category:
            cat_list = "', '".join(content_category)
            where_conditions.append(f"(COALESCE(content_category, '') IN ('{cat_list}') OR content_category IN ('{cat_list}'))")
        if surface:
            surface_list = "', '".join(surface)
            where_conditions.append(f"(COALESCE(surface, 'Unknown') IN ('{surface_list}') OR surface IN ('{surface_list}'))")
        if user_tenure:
            tenure_list = "', '".join(user_tenure)
            where_conditions.append(f"(COALESCE(user_tenure, 'Unknown') IN ('{tenure_list}') OR user_tenure IN ('{tenure_list}'))")
        
        where_clause = " AND ".join(where_conditions)

        # Build SELECT clause with segment dimension if needed
        if segment_by and segment_by in ["user_intent", "surface", "user_tenure", "content_category"]:
            # Use COALESCE for backward compatibility with old events without segment fields
            select_cols = f"user_id, event_type, created_at, COALESCE({segment_by}, 'Unknown') as {segment_by}"
            group_by_col = segment_by
        else:
            select_cols = "user_id, event_type, created_at"
            group_by_col = None

        # Query events from Parquet files
        query = f"""
        SELECT 
            {select_cols}
        FROM read_parquet({files_str})
        WHERE {where_clause}
        ORDER BY user_id, created_at
        """

        # Execute query
        try:
            df = self.conn.execute(query).fetchdf()
        except Exception as e:
            # If query fails, return empty metrics
            print(f"DuckDB query error: {e}")
            empty_result = {stage["name"]: 0 for stage in stages}
            if segment_by:
                return {"segments": {}, "total": empty_result}
            return empty_result

        if df.empty:
            empty_result = {stage["name"]: 0 for stage in stages}
            if segment_by:
                return {"segments": {}, "total": empty_result}
            return empty_result

        # Calculate funnel metrics
        if segment_by and group_by_col and group_by_col in df.columns:
            # Calculate metrics by segment
            segments_result = {}
            # Calculate total from all data (aggregate across all segments, ignoring segment dimension)
            total_df = df[["user_id", "event_type", "created_at"]].copy()
            total_result = self._calculate_stage_counts(total_df, stages)
            
            # Calculate per-segment metrics (exclude "Unknown" and empty segments)
            for segment_value in df[group_by_col].dropna().unique():
                segment_str = str(segment_value).strip()
                # Skip "Unknown" segments and empty strings
                if segment_str == "Unknown" or segment_str == "" or segment_str == "None":
                    continue
                segment_df = df[df[group_by_col] == segment_value][["user_id", "event_type", "created_at"]].copy()
                segment_metrics = self._calculate_stage_counts(segment_df, stages)
                segments_result[segment_str] = segment_metrics
            
            return {
                "segments": segments_result,
                "total": total_result
            }
        else:
            # Calculate aggregate metrics (ensure we only use required columns)
            required_cols = ["user_id", "event_type", "created_at"]
            available_cols = [col for col in required_cols if col in df.columns]
            if not available_cols:
                return {stage["name"]: 0 for stage in stages}
            df_clean = df[available_cols].copy()
            return self._calculate_stage_counts(df_clean, stages)
    
    def _calculate_stage_counts(self, df, stages: List[Dict]) -> Dict[str, int]:
        """Calculate stage counts from dataframe."""
        # Calculate user progression through stages
        user_events = df.groupby("user_id")["event_type"].apply(list).to_dict()

        # Calculate users at each stage
        stage_counts = {}
        for i, stage in enumerate(stages):
            stage_event = stage["event_type"]
            stage_name = stage["name"]
            users_at_stage = set()

            for user_id, user_event_list in user_events.items():
                # Check if user reached this stage
                # User must have completed all previous stages in order
                reached_stage = True

                # Check previous stages were completed
                for prev_stage_idx in range(i):
                    prev_event = stages[prev_stage_idx]["event_type"]
                    if prev_event not in user_event_list:
                        reached_stage = False
                        break

                # Check if current stage event exists
                if reached_stage and stage_event in user_event_list:
                    users_at_stage.add(user_id)

            stage_counts[stage_name] = len(users_at_stage)

        return stage_counts

    def close(self):
        """Close DuckDB connection."""
        self.conn.close()

    def __del__(self):
        """Cleanup on deletion."""
        if hasattr(self, "conn"):
            self.close()
