#!/usr/bin/env python3
"""
Test script for Phase 3 & 4 functionality
Tests project/funnel management and event tracking
"""

import asyncio
import sys
from datetime import datetime
from app.services.project_service import ProjectService
from app.services.funnel_service import FunnelService
from app.services.track_service import TrackService
from app.storage.metadata_handler import MetadataHandler


async def test_phase3():
    """Test Phase 3: Project & Funnel Management."""
    print("=" * 50)
    print("Testing Phase 3: Project & Funnel Management")
    print("=" * 50)
    
    # Test Project Service
    print("\n1. Testing Project Service...")
    project_service = ProjectService()
    
    # Create project
    project = await project_service.create_project(
        org_id="poc-org",
        name="Test Project",
        domain="test.com",
        project_id="test-project-001"
    )
    print(f"✅ Created project: {project['name']} (ID: {project['id']})")
    
    # List projects
    projects = await project_service.list_projects("poc-org")
    print(f"✅ Listed {len(projects)} projects")
    
    # Test Funnel Service
    print("\n2. Testing Funnel Service...")
    funnel_service = FunnelService()
    
    # Create funnel
    stages = [
        {"order": 1, "name": "Page View", "event_type": "page_view"},
        {"order": 2, "name": "Add to Cart", "event_type": "add_to_cart"},
        {"order": 3, "name": "Purchase", "event_type": "purchase"},
    ]
    
    funnel = await funnel_service.create_funnel(
        org_id="poc-org",
        project_id=project["id"],
        name="Test Funnel",
        description="Test funnel for POC",
        stages=stages,
    )
    print(f"✅ Created funnel: {funnel['name']} (ID: {funnel['id']})")
    print(f"   Stages: {len(funnel['stages'])}")
    
    # List funnels
    funnels = await funnel_service.list_funnels("poc-org", project["id"])
    print(f"✅ Listed {len(funnels)} funnels")
    
    return project, funnel


async def test_phase4():
    """Test Phase 4: Event Tracking."""
    print("\n" + "=" * 50)
    print("Testing Phase 4: Event Tracking")
    print("=" * 50)
    
    track_service = TrackService()
    project_id = "test-project-001"
    
    print("\n1. Testing Event Tracking...")
    
    # Track single event
    event_id = await track_service.track_event(
        project_id=project_id,
        event_type="page_view",
        user_id="user1",
        url="https://example.com",
        timestamp=datetime.utcnow().isoformat(),
    )
    print(f"✅ Tracked event: {event_id}")
    
    # Track multiple events
    events = [
        {
            "event_type": "page_view",
            "user_id": "user1",
            "url": "https://example.com",
        },
        {
            "event_type": "add_to_cart",
            "user_id": "user1",
            "url": "https://example.com/cart",
        },
        {
            "event_type": "purchase",
            "user_id": "user1",
            "url": "https://example.com/checkout",
        },
    ]
    
    event_ids = await track_service.track_batch_events(project_id, events)
    print(f"✅ Tracked batch: {len(event_ids)} events")
    
    # Check buffer
    buffer_size = len(track_service.event_buffer.get(project_id, []))
    print(f"✅ Events in buffer: {buffer_size}")
    
    # Flush buffer
    if buffer_size > 0:
        await track_service._flush_buffer(project_id)
        print(f"✅ Flushed buffer to Parquet files")
    
    return project_id


async def main():
    """Run all tests."""
    try:
        # Test Phase 3
        project, funnel = await test_phase3()
        
        # Test Phase 4
        project_id = await test_phase4()
        
        print("\n" + "=" * 50)
        print("✅ Phase 3 & 4 Tests: PASSED")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Check Parquet files in: backend/data/events/")
        print("2. Start server: uvicorn app.main:app --reload")
        print("3. Test API endpoints at: http://localhost:8000/docs")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
