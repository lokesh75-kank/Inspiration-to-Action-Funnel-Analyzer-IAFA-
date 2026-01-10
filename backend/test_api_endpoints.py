#!/usr/bin/env python3
"""
HTTP-based API endpoint testing script
Tests all endpoints via HTTP requests (requires server to be running)
"""

import requests
import json
import sys
from datetime import datetime

API_URL = "http://localhost:8000/api/v1"
BASE_URL = "http://localhost:8000"

# Colors for output
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def test_endpoint(method, url, data=None, headers=None, description=""):
    """Test an API endpoint."""
    print(f"Testing: {description} ... ", end="", flush=True)
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=5)
        else:
            print(f"{Colors.RED}❌ Invalid method{Colors.NC}")
            return False, None
        
        if response.status_code >= 200 and response.status_code < 300:
            print(f"{Colors.GREEN}✅ PASSED{Colors.NC} (HTTP {response.status_code})")
            return True, response.json() if response.content else None
        else:
            print(f"{Colors.RED}❌ FAILED{Colors.NC} (HTTP {response.status_code})")
            try:
                error = response.json()
                print(f"   Error: {error.get('detail', 'Unknown error')}")
            except:
                print(f"   Response: {response.text[:100]}")
            return False, None
            
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}❌ FAILED{Colors.NC} (Connection refused)")
        print(f"   {Colors.YELLOW}Make sure the server is running: uvicorn app.main:app --reload --port 8000{Colors.NC}")
        return False, None
    except Exception as e:
        print(f"{Colors.RED}❌ FAILED{Colors.NC} ({str(e)})")
        return False, None


def main():
    """Run all endpoint tests."""
    print("=" * 60)
    print(f"{Colors.BLUE}IAFA POC - API Endpoint Testing{Colors.NC}")
    print("=" * 60)
    print(f"\n{Colors.YELLOW}Note: Make sure the server is running:{Colors.NC}")
    print("  uvicorn app.main:app --reload --port 8000\n")
    
    passed = 0
    failed = 0
    project_id = None
    funnel_id = None
    
    # Test 1: Health Check
    print("=" * 60)
    print("1. HEALTH CHECK")
    print("=" * 60)
    success, _ = test_endpoint("GET", f"{BASE_URL}/health", description="Health check")
    if success:
        passed += 1
    else:
        failed += 1
        print(f"\n{Colors.RED}Server is not running. Please start it first.{Colors.NC}")
        return False
    
    success, _ = test_endpoint("GET", f"{BASE_URL}/", description="Root endpoint")
    if success:
        passed += 1
    else:
        failed += 1
    
    # Test 2: Projects
    print("\n" + "=" * 60)
    print("2. PROJECT ENDPOINTS")
    print("=" * 60)
    
    success, data = test_endpoint("GET", f"{API_URL}/projects", description="List projects")
    if success:
        passed += 1
        if data and isinstance(data, list) and len(data) > 0:
            project_id = data[0].get("id")
            print(f"   Found project: {data[0].get('name')} (ID: {project_id})")
    else:
        failed += 1
    
    # Create project if none exists
    if not project_id:
        print(f"\n{Colors.YELLOW}No project found, creating one...{Colors.NC}")
        project_data = {"name": "Test Project", "domain": "test.com"}
        success, data = test_endpoint("POST", f"{API_URL}/projects", data=project_data, description="Create project")
        if success and data:
            project_id = data.get("id")
            passed += 1
        else:
            failed += 1
    
    if project_id:
        success, _ = test_endpoint("GET", f"{API_URL}/projects/{project_id}", description="Get project by ID")
        if success:
            passed += 1
        else:
            failed += 1
        
        success, _ = test_endpoint("GET", f"{API_URL}/projects/{project_id}/tracking-code", description="Get tracking code")
        if success:
            passed += 1
        else:
            failed += 1
    
    # Test 3: Funnels
    print("\n" + "=" * 60)
    print("3. FUNNEL ENDPOINTS")
    print("=" * 60)
    
    success, data = test_endpoint("GET", f"{API_URL}/funnels", description="List funnels")
    if success:
        passed += 1
        if data and isinstance(data, list) and len(data) > 0:
            funnel_id = data[0].get("id")
    else:
        failed += 1
    
    # Create funnel
    if project_id:
        print(f"\n{Colors.YELLOW}Creating test funnel...{Colors.NC}")
        funnel_data = {
            "project_id": project_id,
            "name": "Test E-commerce Funnel",
            "description": "Test funnel for POC",
            "stages": [
                {"order": 1, "name": "Page View", "event_type": "page_view"},
                {"order": 2, "name": "Add to Cart", "event_type": "add_to_cart"},
                {"order": 3, "name": "Purchase", "event_type": "purchase"}
            ]
        }
        success, data = test_endpoint("POST", f"{API_URL}/funnels", data=funnel_data, description="Create funnel")
        if success and data:
            funnel_id = data.get("id")
            print(f"   Created funnel: {data.get('name')} (ID: {funnel_id})")
            passed += 1
        else:
            failed += 1
        
        if funnel_id:
            success, _ = test_endpoint("GET", f"{API_URL}/funnels/{funnel_id}", description="Get funnel by ID")
            if success:
                passed += 1
            else:
                failed += 1
    
    # Test 4: Event Tracking
    print("\n" + "=" * 60)
    print("4. EVENT TRACKING ENDPOINTS")
    print("=" * 60)
    
    event_data = {
        "event_type": "page_view",
        "user_id": "user1",
        "url": "https://example.com",
        "properties": {"page": "home"}
    }
    success, _ = test_endpoint("POST", f"{API_URL}/track", data=event_data, description="Track single event")
    if success:
        passed += 1
    else:
        failed += 1
    
    # Batch events
    batch_data = {
        "events": [
            {"event_type": "page_view", "user_id": "user1", "url": "https://example.com"},
            {"event_type": "add_to_cart", "user_id": "user1", "url": "https://example.com/cart"},
            {"event_type": "purchase", "user_id": "user1", "url": "https://example.com/checkout"}
        ]
    }
    success, data = test_endpoint("POST", f"{API_URL}/track/batch", data=batch_data, description="Track batch events")
    if success:
        passed += 1
        if data:
            print(f"   Processed {data.get('events_processed', 0)} events")
    else:
        failed += 1
    
    # Test 5: Analytics
    print("\n" + "=" * 60)
    print("5. ANALYTICS ENDPOINTS")
    print("=" * 60)
    
    if funnel_id:
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"{API_URL}/analytics/funnel/{funnel_id}?start_date={today}&end_date={today}"
        success, data = test_endpoint("GET", url, description="Get funnel analytics")
        if success:
            passed += 1
            if data:
                print(f"   Funnel: {data.get('funnel_name')}")
                print(f"   Total users: {data.get('total_users', 0)}")
                print(f"   Conversion rate: {data.get('overall_conversion_rate', 0)}%")
        else:
            failed += 1
    else:
        print(f"{Colors.YELLOW}⚠️  Skipping analytics test (no funnel ID){Colors.NC}")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"{Colors.GREEN}Passed: {passed}{Colors.NC}")
    print(f"{Colors.RED}Failed: {failed}{Colors.NC}")
    print()
    
    if failed == 0:
        print(f"{Colors.GREEN}✅ ALL TESTS PASSED!{Colors.NC}")
        print("\nNext steps:")
        print("1. Visit API docs: http://localhost:8000/docs")
        print("2. Test endpoints interactively via Swagger UI")
        print("3. Check Parquet files in: backend/data/events/")
        return True
    else:
        print(f"{Colors.RED}❌ SOME TESTS FAILED{Colors.NC}")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.NC}")
        sys.exit(1)
