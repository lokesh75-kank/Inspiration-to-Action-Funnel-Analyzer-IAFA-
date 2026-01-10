#!/bin/bash

# IAFA POC - API Endpoint Testing Script
# Tests all endpoints via HTTP requests

API_URL="http://localhost:8000/api/v1"
BASE_URL="http://localhost:8000"

echo "=========================================="
echo "IAFA POC - API Endpoint Testing"
echo "=========================================="
echo ""
echo "Make sure the server is running:"
echo "  uvicorn app.main:app --reload --port 8000"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    
    echo -n "Testing: $description ... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$endpoint")
    elif [ "$method" = "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST "$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    elif [ "$method" = "PUT" ]; then
        response=$(curl -s -w "\n%{http_code}" -X PUT "$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    elif [ "$method" = "DELETE" ]; then
        response=$(curl -s -w "\n%{http_code}" -X DELETE "$endpoint")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✅ PASSED${NC} (HTTP $http_code)"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ FAILED${NC} (HTTP $http_code)"
        echo "   Response: $body"
        ((FAILED++))
        return 1
    fi
}

# Test 1: Health Check
echo "=========================================="
echo "1. HEALTH CHECK"
echo "=========================================="
test_endpoint "GET" "$BASE_URL/health" "" "Health check"

# Test 2: Root endpoint
test_endpoint "GET" "$BASE_URL/" "" "Root endpoint"

# Test 3: List Projects
echo ""
echo "=========================================="
echo "2. PROJECT ENDPOINTS"
echo "=========================================="
test_endpoint "GET" "$API_URL/projects" "" "List projects"

# Get project ID from response
PROJECT_RESPONSE=$(curl -s "$API_URL/projects")
PROJECT_ID=$(echo "$PROJECT_RESPONSE" | grep -o '"id":"[^"]*' | head -1 | cut -d'"' -f4)

if [ -z "$PROJECT_ID" ]; then
    echo -e "${YELLOW}⚠️  No project found, creating one...${NC}"
    CREATE_RESPONSE=$(curl -s -X POST "$API_URL/projects" \
        -H "Content-Type: application/json" \
        -d '{"name": "Test Project", "domain": "test.com"}')
    PROJECT_ID=$(echo "$CREATE_RESPONSE" | grep -o '"id":"[^"]*' | head -1 | cut -d'"' -f4)
    echo "Created project: $PROJECT_ID"
fi

if [ -n "$PROJECT_ID" ]; then
    test_endpoint "GET" "$API_URL/projects/$PROJECT_ID" "" "Get project by ID"
    test_endpoint "GET" "$API_URL/projects/$PROJECT_ID/tracking-code" "" "Get tracking code"
fi

# Test 4: Funnel Endpoints
echo ""
echo "=========================================="
echo "3. FUNNEL ENDPOINTS"
echo "=========================================="
test_endpoint "GET" "$API_URL/funnels" "" "List funnels"

# Create a funnel
FUNNEL_DATA='{
  "project_id": "'$PROJECT_ID'",
  "name": "Test Funnel",
  "description": "Test funnel for POC",
  "stages": [
    {"order": 1, "name": "Page View", "event_type": "page_view"},
    {"order": 2, "name": "Add to Cart", "event_type": "add_to_cart"},
    {"order": 3, "name": "Purchase", "event_type": "purchase"}
  ]
}'

CREATE_FUNNEL_RESPONSE=$(curl -s -X POST "$API_URL/funnels" \
    -H "Content-Type: application/json" \
    -d "$FUNNEL_DATA")

FUNNEL_ID=$(echo "$CREATE_FUNNEL_RESPONSE" | grep -o '"id":"[^"]*' | head -1 | cut -d'"' -f4)

if [ -n "$FUNNEL_ID" ]; then
    echo -e "${GREEN}✅ Created funnel: $FUNNEL_ID${NC}"
    test_endpoint "GET" "$API_URL/funnels/$FUNNEL_ID" "" "Get funnel by ID"
else
    echo -e "${RED}❌ Failed to create funnel${NC}"
fi

# Test 5: Event Tracking
echo ""
echo "=========================================="
echo "4. EVENT TRACKING ENDPOINTS"
echo "=========================================="

EVENT_DATA='{
  "event_type": "page_view",
  "user_id": "user1",
  "url": "https://example.com",
  "properties": {"page": "home"}
}'

test_endpoint "POST" "$API_URL/track" "$EVENT_DATA" "Track single event"

# Track batch events
BATCH_DATA='{
  "events": [
    {"event_type": "page_view", "user_id": "user1", "url": "https://example.com"},
    {"event_type": "add_to_cart", "user_id": "user1", "url": "https://example.com/cart"},
    {"event_type": "purchase", "user_id": "user1", "url": "https://example.com/checkout"}
  ]
}'

test_endpoint "POST" "$API_URL/track/batch" "$BATCH_DATA" "Track batch events"

# Test 6: Analytics
echo ""
echo "=========================================="
echo "5. ANALYTICS ENDPOINTS"
echo "=========================================="

if [ -n "$FUNNEL_ID" ]; then
    TODAY=$(date +%Y-%m-%d)
    test_endpoint "GET" "$API_URL/analytics/funnel/$FUNNEL_ID?start_date=$TODAY&end_date=$TODAY" "" "Get funnel analytics"
else
    echo -e "${YELLOW}⚠️  Skipping analytics test (no funnel ID)${NC}"
fi

# Summary
echo ""
echo "=========================================="
echo "TEST SUMMARY"
echo "=========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED!${NC}"
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    exit 1
fi
