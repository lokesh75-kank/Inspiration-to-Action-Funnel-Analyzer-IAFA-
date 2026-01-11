#!/usr/bin/env python3
"""
Pre-populate sample data for IAFA Demo
Creates events with common Pinterest event types: pin_view, save, click, purchase
"""

import asyncio
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.track_service import TrackService
from app.services.project_service import ProjectService

# Default project ID (from backend/app/api/v1/projects.py)
DEFAULT_PROJECT_ID = "poc-project-001"

async def populate_sample_data():
    """Pre-populate sample events with common Pinterest event types."""
    
    print("📊 Pre-populating sample data for IAFA Demo...")
    print("=" * 60)
    
    # Initialize services
    project_service = ProjectService()
    track_service = TrackService()
    
    # Get or create default project
    try:
        project = await project_service.get_project_by_id(DEFAULT_PROJECT_ID)
        if not project:
            print(f"Creating default project...")
            project = await project_service.create_project(
                org_id="poc-org",
                name="Pinterest",
                domain="Home Feed",
                project_id=DEFAULT_PROJECT_ID
            )
        project_id = project['id']
        print(f"✅ Using project: {project['name']} (ID: {project_id})")
    except Exception as e:
        print(f"❌ Error getting project: {e}")
        return
    
    print("\n📝 Generating events...")
    
    # Common Pinterest events to populate
    events_to_generate = [
        ('pin_view', 'save', 'click', 'purchase'),  # Full journey
    ]
    
    base_date = datetime.now() - timedelta(days=7)  # Spread over last 7 days
    
    total_events = 0
    
    # Planner users - High save rate (60%), lower click rate (30%)
    print("\n👥 Generating Planner user events...")
    for i in range(1, 101):
        user_id = f"planner_user_{i}"
        event_date = base_date + timedelta(days=(i % 7))
        
        # Pin View (all planners)
        await track_service.track_event(
            project_id=project_id,
            event_type='pin_view',
            user_id=user_id,
            user_intent='Planner',
            surface='Home',
            user_tenure='Retained',
            content_category='home_decor',
            timestamp=event_date.isoformat()
        )
        total_events += 1
        
        # Save (60% of planners)
        if i <= 60:
            await track_service.track_event(
                project_id=project_id,
                event_type='save',
                user_id=user_id,
                user_intent='Planner',
                surface='Home',
                user_tenure='Retained',
                content_category='home_decor',
                timestamp=(event_date + timedelta(minutes=5)).isoformat()
            )
            total_events += 1
        
        # Click (30% of planners - they save for later, click less)
        if i <= 30:
            await track_service.track_event(
                project_id=project_id,
                event_type='click',
                user_id=user_id,
                user_intent='Planner',
                user_tenure='Retained',
                content_category='home_decor',
                timestamp=(event_date + timedelta(minutes=10)).isoformat()
            )
            total_events += 1
        
        # Purchase (15% of planners - they plan first, then purchase later)
        if i <= 15:
            await track_service.track_event(
                project_id=project_id,
                event_type='purchase',
                user_id=user_id,
                user_intent='Planner',
                user_tenure='Retained',
                content_category='home_decor',
                timestamp=(event_date + timedelta(hours=2)).isoformat()
            )
            total_events += 1
    
    # Actor users - Lower save rate (40%), higher click rate (50%), higher purchase (25%)
    # Mix: 80 Retained, 20 New (New users have lower engagement)
    print("👥 Generating Actor user events...")
    for i in range(1, 101):
        user_id = f"actor_user_{i}"
        event_date = base_date + timedelta(days=(i % 7))
        # First 80 are Retained, last 20 are New
        user_tenure = 'Retained' if i <= 80 else 'New'
        
        # Pin View (all actors)
        await track_service.track_event(
            project_id=project_id,
            event_type='pin_view',
            user_id=user_id,
            user_intent='Actor',
            surface='Home',
            user_tenure=user_tenure,
            content_category='shopping',
            timestamp=event_date.isoformat()
        )
        total_events += 1
        
        # Save (40% of retained actors, 20% of new actors - new users less engaged)
        save_threshold = 40 if i <= 80 else 4  # 40% of 80 = 32, 20% of 20 = 4
        if (i <= 80 and i <= 40) or (i > 80 and i <= 84):
            await track_service.track_event(
                project_id=project_id,
                event_type='save',
                user_id=user_id,
                user_intent='Actor',
                surface='Home',
                user_tenure=user_tenure,
                content_category='shopping',
                timestamp=(event_date + timedelta(minutes=2)).isoformat()
            )
            total_events += 1
        
        # Click (50% of retained actors, 30% of new actors)
        click_threshold = 50 if i <= 80 else 6  # 50% of 80 = 40, 30% of 20 = 6
        if (i <= 80 and i <= 50) or (i > 80 and i <= 86):
            await track_service.track_event(
                project_id=project_id,
                event_type='click',
                user_id=user_id,
                user_intent='Actor',
                user_tenure=user_tenure,
                content_category='shopping',
                timestamp=(event_date + timedelta(minutes=3)).isoformat()
            )
            total_events += 1
        
        # Purchase (25% of retained actors, 10% of new actors)
        purchase_threshold = 25 if i <= 80 else 2  # 25% of 80 = 20, 10% of 20 = 2
        if (i <= 80 and i <= 25) or (i > 80 and i <= 82):
            await track_service.track_event(
                project_id=project_id,
                event_type='purchase',
                user_id=user_id,
                user_intent='Actor',
                user_tenure=user_tenure,
                content_category='shopping',
                timestamp=(event_date + timedelta(minutes=5)).isoformat()
            )
            total_events += 1
    
    # Add some New Planner users (30 New Planners - lower engagement)
    print("👥 Generating New Planner user events...")
    for i in range(1, 31):
        user_id = f"new_planner_user_{i}"
        event_date = base_date + timedelta(days=(i % 7))
        
        # Pin View (all new planners)
        await track_service.track_event(
            project_id=project_id,
            event_type='pin_view',
            user_id=user_id,
            user_intent='Planner',
            surface='Home',
            user_tenure='New',
            content_category='home_decor',
            timestamp=event_date.isoformat()
        )
        total_events += 1
        
        # Save (40% of new planners - lower than retained)
        if i <= 12:  # 40% of 30 = 12
            await track_service.track_event(
                project_id=project_id,
                event_type='save',
                user_id=user_id,
                user_intent='Planner',
                surface='Home',
                user_tenure='New',
                content_category='home_decor',
                timestamp=(event_date + timedelta(minutes=5)).isoformat()
            )
            total_events += 1
        
        # Click (15% of new planners - lower engagement)
        if i <= 5:  # 15% of 30 = 4.5, round to 5
            await track_service.track_event(
                project_id=project_id,
                event_type='click',
                user_id=user_id,
                user_intent='Planner',
                user_tenure='New',
                content_category='home_decor',
                timestamp=(event_date + timedelta(minutes=10)).isoformat()
            )
            total_events += 1
        
        # Purchase (5% of new planners - very low)
        if i <= 2:  # 5% of 30 = 1.5, round to 2
            await track_service.track_event(
                project_id=project_id,
                event_type='purchase',
                user_id=user_id,
                user_intent='Planner',
                user_tenure='New',
                content_category='home_decor',
                timestamp=(event_date + timedelta(hours=2)).isoformat()
            )
            total_events += 1
    
    # Flush any remaining events in buffer
    await track_service._flush_buffer(project_id)
    
    print(f"\n✅ Generated {total_events} events")
    print("\n📊 Event Summary:")
    print("   - pin_view: 230 events (130 Planners [100 Retained + 30 New] + 100 Actors [80 Retained + 20 New])")
    print("   - save: ~100 events (60 Retained Planners + 12 New Planners + 32 Retained Actors + 4 New Actors)")
    print("   - click: ~80 events (30 Retained Planners + 5 New Planners + 40 Retained Actors + 6 New Actors)")
    print("   - purchase: ~40 events (15 Retained Planners + 2 New Planners + 20 Retained Actors + 2 New Actors)")
    print("\n👥 User Tenure Breakdown:")
    print("   - Retained: 180 users (100 Planners + 80 Actors)")
    print("   - New: 50 users (30 Planners + 20 Actors)")
    
    print("\n🎯 Available Event Types:")
    print("   - pin_view")
    print("   - save")
    print("   - click")
    print("   - purchase")
    
    print("\n📋 Suggested Journeys:")
    print("   1. pin_view → save (most common)")
    print("   2. pin_view → save → click")
    print("   3. pin_view → click")
    print("   4. pin_view → save → click → purchase")
    
    print("\n✅ Sample data pre-populated successfully!")
    print("   You can now create journeys using these event types in the UI.")

if __name__ == "__main__":
    asyncio.run(populate_sample_data())
