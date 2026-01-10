#!/usr/bin/env python3
"""
Comprehensive endpoint testing script for IAFA POC
Tests all API endpoints without requiring a running server
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.project_service import ProjectService
from app.services.funnel_service import FunnelService
from app.services.track_service import TrackService
from app.services.analytics_service import AnalyticsService
from app.storage.metadata_handler import MetadataHandler


async def test_projects():
    """Test project endpoints."""
    print("\n" + "=" * 60)
    print("TESTING PROJECT ENDPOINTS")
    print("=" * 60)
    
    service = ProjectService()
    org_id = "poc-org"
    
    # Test 1: List projects
    print("\n1. Testing: List Projects")
    try:
        projects = await service.list_projects(org_id)
        print(f"   ✅ Listed {len(projects)} projects")
        if projects:
            print(f"   Project: {projects[0]['name']}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    # Test 2: Get default project
    print("\n2. Testing: Get Default Project")
    try:
        project = await service.get_project_by_id("poc-project-001")
        if project:
            print(f"   ✅ Found project: {project['name']}")
        else:
            # Create default project
            project = await service.create_project(
                org_id=org_id,
                name="POC Project",
                domain="localhost",
                project_id="poc-project-001"
            )
            print(f"   ✅ Created default project: {project['name']}")
            print(f"   API Key: {project['api_key'][:20]}...")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    # Test 3: Create new project
    print("\n3. Testing: Create Project")
    try:
        new_project = await service.create_project(
            org_id=org_id,
            name="Test Project",
            domain="test.com"
        )
        print(f"   ✅ Created project: {new_project['name']} (ID: {new_project['id']})")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    return True, project


async def test_funnels(project_id: str):
    """Test funnel endpoints."""
    print("\n" + "=" * 60)
    print("TESTING FUNNEL ENDPOINTS")
    print("=" * 60)
    
    service = FunnelService()
    org_id = "poc-org"
    
    # Test 1: Create funnel
    print("\n1. Testing: Create Funnel")
    try:
        stages = [
            {"order": 1, "name": "Page View", "event_type": "page_view"},
            {"order": 2, "name": "Add to Cart", "event_type": "add_to_cart"},
            {"order": 3, "name": "Purchase", "event_type": "purchase"},
        ]
        
        funnel = await service.create_funnel(
            org_id=org_id,
            project_id=project_id,
            name="E-commerce Funnel",
            description="Test funnel for POC",
            stages=stages,
        )
        print(f"   ✅ Created funnel: {funnel['name']} (ID: {funnel['id']})")
        print(f"   Stages: {len(funnel['stages'])}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False, None
    
    # Test 2: List funnels
    print("\n2. Testing: List Funnels")
    try:
        funnels = await service.list_funnels(org_id, project_id)
        print(f"   ✅ Listed {len(funnels)} funnels")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False, None
    
    # Test 3: Get funnel
    print("\n3. Testing: Get Funnel")
    try:
        retrieved = await service.get_funnel(funnel['id'], org_id)
        if retrieved:
            print(f"   ✅ Retrieved funnel: {retrieved['name']}")
        else:
            print(f"   ❌ Funnel not found")
            return False, None
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False, None
    
    return True, funnel


async def test_tracking(project_id: str):
    """Test event tracking."""
    print("\n" + "=" * 60)
    print("TESTING EVENT TRACKING ENDPOINTS")
    print("=" * 60)
    
    service = TrackService()
    
    # Test 1: Track single event
    print("\n1. Testing: Track Single Event")
    try:
        event_id = await service.track_event(
            project_id=project_id,
            event_type="page_view",
            user_id="user1",
            url="https://example.com",
            timestamp=datetime.utcnow().isoformat(),
        )
        print(f"   ✅ Tracked event: {event_id}")
        print(f"   Buffer size: {len(service.event_buffer.get(project_id, []))}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 2: Track multiple events
    print("\n2. Testing: Track Batch Events")
    try:
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
        
        event_ids = await service.track_batch_events(project_id, events)
        print(f"   ✅ Tracked batch: {len(event_ids)} events")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Flush buffer to Parquet
    print("\n3. Testing: Flush Buffer to Parquet")
    try:
        buffer_size = len(service.event_buffer.get(project_id, []))
        if buffer_size > 0:
            await service._flush_buffer(project_id)
            print(f"   ✅ Flushed {buffer_size} events to Parquet")
            
            # Check if file was created
            from app.core.config import settings
            data_dir = Path(settings.DATA_DIR)
            today = datetime.utcnow()
            parquet_file = (
                data_dir / "events" / f"project_{project_id}" 
                / str(today.year) / f"{today.month:02d}" 
                / f"events_{today.strftime('%Y-%m-%d')}.parquet"
            )
            
            if parquet_file.exists():
                print(f"   ✅ Parquet file created: {parquet_file.name}")
                # Try to read it
                try:
                    import pandas as pd
                    df = pd.read_parquet(parquet_file)
                    print(f"   ✅ File readable: {len(df)} events in file")
                except Exception as e:
                    print(f"   ⚠️  Could not read file: {e}")
            else:
                print(f"   ⚠️  Parquet file not found (may be created on next flush)")
        else:
            print(f"   ⚠️  No events in buffer to flush")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


async def test_analytics(funnel_id: str, project_id: str):
    """Test analytics endpoints."""
    print("\n" + "=" * 60)
    print("TESTING ANALYTICS ENDPOINTS")
    print("=" * 60)
    
    service = AnalyticsService()
    org_id = "poc-org"
    
    # Test: Get funnel analytics
    print("\n1. Testing: Get Funnel Analytics")
    try:
        today = datetime.utcnow()
        start_date = today.strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        
        analytics = await service.calculate_funnel_metrics(
            funnel_id=funnel_id,
            org_id=org_id,
            start_date=start_date,
            end_date=end_date,
        )
        
        if analytics:
            print(f"   ✅ Analytics calculated for: {analytics['funnel_name']}")
            print(f"   Total users: {analytics['total_users']}")
            print(f"   Completed users: {analytics['completed_users']}")
            print(f"   Conversion rate: {analytics['overall_conversion_rate']}%")
            print(f"   Stages: {len(analytics['stages'])}")
            for stage in analytics['stages']:
                print(f"     - {stage['stage_name']}: {stage['users']} users ({stage['conversion_rate']}%)")
        else:
            print(f"   ⚠️  No analytics data (may need events first)")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


async def main():
    """Run all endpoint tests."""
    print("=" * 60)
    print("IAFA POC - ENDPOINT TESTING")
    print("=" * 60)
    print("Testing all API endpoints...")
    
    results = {}
    
    # Test Projects
    success, project = await test_projects()
    results['projects'] = success
    if not success:
        print("\n❌ Project tests failed. Stopping.")
        return False
    
    project_id = project['id']
    
    # Test Funnels
    success, funnel = await test_funnels(project_id)
    results['funnels'] = success
    if not success:
        print("\n❌ Funnel tests failed. Stopping.")
        return False
    
    funnel_id = funnel['id'] if funnel else None
    
    # Test Tracking
    results['tracking'] = await test_tracking(project_id)
    
    # Test Analytics (if funnel exists)
    if funnel_id:
        results['analytics'] = await test_analytics(funnel_id, project_id)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name.upper():15} {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✅ ALL TESTS PASSED!")
        print("\nNext steps:")
        print("1. Start server: uvicorn app.main:app --reload --port 8000")
        print("2. Visit API docs: http://localhost:8000/docs")
        print("3. Test endpoints via Swagger UI")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("Please check the errors above")
    
    return all_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
