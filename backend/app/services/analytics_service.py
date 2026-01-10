"""Analytics service."""

from typing import Optional, Dict, List
from app.storage.metadata_handler import MetadataHandler
from app.storage.duckdb_query import DuckDBQuery


class AnalyticsService:
    """Service for funnel analytics."""

    def __init__(self):
        self.metadata_handler = MetadataHandler()
        self.duckdb_query = DuckDBQuery()

    async def calculate_funnel_metrics(
        self, 
        funnel_id: str, 
        org_id: str, 
        start_date: str, 
        end_date: str,
        # Segment filters (Phase 2)
        user_intent: List[str] = None,
        content_category: List[str] = None,
        surface: List[str] = None,
        user_tenure: List[str] = None,
        # Segment breakdown
        segment_by: str = None,
    ) -> Optional[Dict]:
        """Calculate funnel metrics for a date range with segment filtering support."""
        # Load funnel definition
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

        # Calculate metrics using DuckDB with segment filters
        metrics_result = self.duckdb_query.calculate_funnel_metrics(
            funnel_id=funnel_id,
            project_id=funnel["project_id"],
            stages=funnel["stages"],
            start_date=start_date,
            end_date=end_date,
            user_intent=user_intent,
            content_category=content_category,
            surface=surface,
            user_tenure=user_tenure,
            segment_by=segment_by,
        )

        # Check if we have segment breakdown
        if isinstance(metrics_result, dict) and "segments" in metrics_result:
            # Segment breakdown mode
            segments_metrics = {}
            for segment_value, segment_metrics in metrics_result["segments"].items():
                stage_metrics = self._format_stage_metrics(segment_metrics, funnel["stages"])
                segments_metrics[segment_value] = {
                    "stages": stage_metrics,
                    "total_users": stage_metrics[0]["users"] if stage_metrics else 0,
                    "completed_users": stage_metrics[-1]["users"] if stage_metrics else 0,
                    "overall_conversion_rate": stage_metrics[-1]["conversion_rate"] if stage_metrics else 0,
                }
            
            # Total metrics (aggregated across all segments)
            total_metrics = self._format_stage_metrics(metrics_result["total"], funnel["stages"])
            total_users = total_metrics[0]["users"] if total_metrics else 0
            completed_users = total_metrics[-1]["users"] if total_metrics else 0
            overall_conversion = total_metrics[-1]["conversion_rate"] if total_metrics else 0
            
            return {
                "funnel_id": funnel_id,
                "funnel_name": funnel["name"],
                "date_range": {"start": start_date, "end": end_date},
                "segment_by": segment_by,
                "segments": segments_metrics,
                "total": {
                    "stages": total_metrics,
                    "total_users": total_users,
                    "completed_users": completed_users,
                    "overall_conversion_rate": overall_conversion,
                },
            }
        else:
            # Aggregate mode (no segment breakdown)
            metrics = metrics_result
            stage_metrics = self._format_stage_metrics(metrics, funnel["stages"])
            
            overall_conversion = stage_metrics[-1]["conversion_rate"] if stage_metrics else 0
            total_users = stage_metrics[0]["users"] if stage_metrics else 0
            completed_users = stage_metrics[-1]["users"] if stage_metrics else 0

            return {
                "funnel_id": funnel_id,
                "funnel_name": funnel["name"],
                "date_range": {"start": start_date, "end": end_date},
                "stages": stage_metrics,
                "overall_conversion_rate": overall_conversion,
                "total_users": total_users,
                "completed_users": completed_users,
            }
    
    def _format_stage_metrics(self, metrics: Dict[str, int], stages: List[Dict]) -> List[Dict]:
        """Format stage metrics from raw counts."""
        stage_metrics = []
        prev_count = None
        first_stage_count = metrics.get(stages[0]["name"], 0) if stages else 0

        for i, stage in enumerate(stages):
            stage_name = stage["name"]
            users = metrics.get(stage_name, 0)
            conversion_rate = (users / first_stage_count * 100) if first_stage_count > 0 else 0
            drop_off_rate = ((prev_count - users) / prev_count * 100) if prev_count and prev_count > 0 else 0

            stage_metrics.append(
                {
                    "stage_name": stage_name,
                    "stage_order": stage["order"],
                    "users": users,
                    "conversion_rate": round(conversion_rate, 2),
                    "drop_off_rate": round(drop_off_rate, 2),
                }
            )
            prev_count = users

        return stage_metrics
