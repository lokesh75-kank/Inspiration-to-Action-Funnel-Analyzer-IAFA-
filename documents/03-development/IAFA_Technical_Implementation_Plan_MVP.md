# IAFA - Technical Implementation Plan (MVP)

## Document Overview

**Purpose**: Detailed technical implementation guide for the Inspiration-to-Action Funnel Analyzer MVP  
**Version**: 2.0  
**Target Timeline**: 6-8 weeks (reduced due to simpler file-based storage)  
**Status**: Planning Phase  
**Storage**: Parquet files with DuckDB (file-based analytics - no database required)

---

## 1. MVP Scope Definition

### 1.1 Core Features (Must-Have)

1. **Event Tracking**
   - JavaScript SDK for web tracking
   - Track custom events (page views, clicks, conversions)
   - User identification (anonymous & authenticated)

2. **Funnel Definition**
   - Pre-defined funnel templates
   - Custom funnel creation (up to 5 stages)
   - Stage-based event mapping

3. **Basic Analytics Dashboard**
   - Funnel visualization (funnel chart)
   - Conversion rates by stage
   - Drop-off percentages
   - Date range filtering (last 7/30/90 days, custom range)

4. **Data Collection API**
   - RESTful API for event ingestion
   - Batch event support
   - Event validation

5. **User Management**
   - Basic authentication (email/password)
   - Multi-tenant support (organizations)
   - Single project per organization (MVP limitation)

### 1.2 Out of Scope (Future Releases)

- Real-time analytics (batch processing only for MVP)
- Advanced segmentation
- Cohort analysis
- Machine learning predictions
- Export functionality (PDF, CSV)
- Scheduled reports
- Email notifications
- A/B test integration

---

## 2. Technology Stack

### 2.1 Backend

**Primary Stack**:
- **Language**: Python 3.11+
- **Framework**: FastAPI (high performance, async support, auto-docs)
- **Data Storage**: Parquet files (columnar storage for analytics)
- **Query Engine**: DuckDB (embedded analytics database - queries Parquet directly)
- **Cache**: Redis 7+ (optional, for rate limiting, sessions) OR in-memory caching
- **Task Queue**: Optional - can use simple async tasks or ThreadPoolExecutor for MVP

**Additional Libraries**:
- `pydantic`: Data validation
- `duckdb`: Embedded analytics database (queries Parquet files)
- `pyarrow`: Parquet file read/write operations
- `pandas`: Data analysis (works seamlessly with Parquet and DuckDB)
- `python-jose[cryptography]`: JWT authentication
- `passlib[bcrypt]`: Password hashing
- `python-multipart`: File uploads
- `aiofiles`: Async file operations
- `redis`: Redis client (optional for MVP - can use file-based session storage)

### 2.2 Frontend

**Primary Stack**:
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **State Management**: Zustand (lightweight, simple)
- **HTTP Client**: Axios
- **Routing**: React Router v6
- **UI Library**: Tailwind CSS + shadcn/ui (modern, customizable)
- **Charts**: Recharts (React-native charting library)
- **Date Picker**: react-datepicker
- **Form Handling**: React Hook Form + Zod validation

### 2.3 Infrastructure

- **Containerization**: Docker + Docker Compose (local dev) - simplified (no database container needed)
- **Storage**: Local file system or cloud storage (S3, GCS) for Parquet files
- **Web Server**: Nginx (reverse proxy for production) or skip for MVP
- **Process Manager**: Gunicorn with Uvicorn workers (FastAPI) or Uvicorn directly for MVP
- **Monitoring**: Basic logging (MVP - no external monitoring tools)
- **File Management**: Directory structure for organizing Parquet files by project/date

### 2.4 Development Tools

- **Version Control**: Git
- **Code Quality**: 
  - Backend: Black, isort, mypy, pylint
  - Frontend: ESLint, Prettier
- **Testing**:
  - Backend: pytest, pytest-asyncio, pytest-cov
  - Frontend: Vitest, React Testing Library

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────┐
│   Web Browser   │
│   (React App)   │
└────────┬────────┘
         │
         │ HTTPS
         │
┌────────▼────────┐
│   FastAPI App   │
│  (Single Server)│
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────────────┐
│DuckDB │ │  Parquet Files  │
│Query  │ │  (Event Data)   │
│Engine │ │  (Metadata)     │
└───┬───┘ └─────────────────┘
    │
    │
┌───▼───────────────────┐
│  File System Storage  │
│  - events/*.parquet   │
│  - metadata/*.json    │
│  - config/*.json      │
└───────────────────────┘
```

### 3.2 Component Architecture

**Backend Services**:
1. **API Service** (FastAPI - single service for MVP)
   - Authentication endpoints (file-based user storage - JSON)
   - Event ingestion endpoints (write to Parquet)
   - Analytics query endpoints (query Parquet via DuckDB)
   - Project/funnel management endpoints (JSON config files)

2. **Storage Layer** (File-based)
   - **Parquet Files**: Event data (partitioned by project_id and date)
   - **JSON Files**: Metadata (users, projects, funnels, config)
   - **DuckDB**: Embedded query engine (queries Parquet files directly)
   - **File Structure**:
     ```
     data/
     ├── events/
     │   ├── project_{id}/
     │   │   ├── 2024/
     │   │   │   ├── 01/
     │   │   │   │   ├── events_2024-01-15.parquet
     │   │   │   │   └── events_2024-01-16.parquet
     │   │   │   └── ...
     │   │   └── ...
     │   └── ...
     ├── metadata/
     │   ├── users.json
     │   ├── projects.json
     │   └── funnels.json
     └── config/
         └── app_config.json
     ```

3. **Processing** (In-memory/Async for MVP)
   - Event validation and Parquet writing (async I/O)
   - Funnel calculations (DuckDB queries)
   - Optional: Background tasks with asyncio or ThreadPoolExecutor

**Frontend Application**:
1. **Dashboard**
   - Funnel visualization
   - Metrics display
   - Date range selector

2. **Management Pages**
   - Login/Signup
   - Project settings
   - Funnel configuration
   - Event tracking code generator

---

## 4. Data Storage Schema

### 4.1 File Structure

#### Directory Layout
```
iafa_data/
├── events/                          # Event data (Parquet files)
│   └── project_{project_id}/
│       └── {year}/
│           └── {month}/
│               └── events_{date}.parquet  # Daily partitions
├── metadata/                        # JSON metadata files
│   ├── users.json                   # User accounts
│   ├── projects.json                # Project configurations
│   └── funnels.json                 # Funnel definitions
└── config/
    └── app_config.json              # Application configuration
```

### 4.2 Event Data Schema (Parquet)

**File**: `events/project_{id}/{year}/{month}/events_{date}.parquet`

**Columns** (Parquet schema):
```python
{
    "id": "string",              # UUID
    "project_id": "string",      # Project identifier
    "event_type": "string",      # 'page_view', 'click', 'purchase', etc.
    "user_id": "string",         # Anonymous or authenticated user ID
    "session_id": "string",      # Session identifier
    "properties": "map<string,string>",  # Event metadata (key-value pairs)
    "url": "string",             # Page URL
    "referrer": "string",        # Referrer URL
    "user_agent": "string",      # User agent string
    "ip_address": "string",      # IP address (hashed for privacy)
    "created_at": "timestamp",   # Event timestamp (UTC)
}
```

**Parquet File Properties**:
- Compression: Snappy or Gzip (for better compression ratio)
- Partitioning: By project_id, year, month, date (partition pruning for fast queries)
- Row group size: ~128MB (optimized for analytics queries)
- Write: Batch writes (append events, write daily file)

### 4.3 Metadata Files (JSON)

#### `metadata/users.json`
```json
{
    "users": [
        {
            "id": "uuid",
            "email": "user@example.com",
            "password_hash": "bcrypt_hash",
            "full_name": "John Doe",
            "organization_id": "uuid",
            "role": "owner",
            "is_active": true,
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z"
        }
    ]
}
```

#### `metadata/projects.json`
```json
{
    "projects": [
        {
            "id": "uuid",
            "organization_id": "uuid",
            "name": "My Project",
            "api_key": "hash_value",
            "domain": "example.com",
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z"
        }
    ]
}
```

#### `metadata/funnels.json`
```json
{
    "funnels": [
        {
            "id": "uuid",
            "project_id": "uuid",
            "name": "E-commerce Funnel",
            "description": "Purchase funnel",
            "stages": [
                {
                    "name": "Page View",
                    "event": "page_view",
                    "order": 1
                },
                {
                    "name": "Add to Cart",
                    "event": "add_to_cart",
                    "order": 2
                },
                {
                    "name": "Purchase",
                    "event": "purchase",
                    "order": 3
                }
            ],
            "is_active": true,
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z"
        }
    ]
}
```

### 4.4 DuckDB Usage

**Query Parquet Files Directly**:
```python
import duckdb

# Connect to DuckDB (in-memory by default for MVP)
conn = duckdb.connect()

# Query Parquet files directly
query = """
SELECT 
    event_type,
    COUNT(*) as count,
    COUNT(DISTINCT user_id) as unique_users
FROM 'data/events/project_123/2024/01/*.parquet'
WHERE created_at >= '2024-01-15'
  AND created_at < '2024-01-16'
GROUP BY event_type
"""

result = conn.execute(query).fetchdf()
```

**Benefits**:
- No database setup required
- Fast columnar queries (Parquet is columnar format)
- Automatic partition pruning (filters files by path)
- SQL-like interface
- Can aggregate across multiple Parquet files

### 4.5 Data Retention Strategy (MVP)

- **Raw Events**: Store in Parquet files for 90 days, then delete old files
- **Metadata**: Keep indefinitely (JSON files are small)
- **Cleanup**: Daily job to delete files older than retention period
- **Backup**: Optionally compress old Parquet files before deletion

---

## 5. API Endpoints

### 5.1 Authentication Endpoints

```
POST   /api/v1/auth/register          # Register new user
POST   /api/v1/auth/login             # Login
POST   /api/v1/auth/refresh           # Refresh JWT token
POST   /api/v1/auth/logout            # Logout
GET    /api/v1/auth/me                # Get current user
```

### 5.2 Project Management

```
GET    /api/v1/projects               # List projects
POST   /api/v1/projects               # Create project
GET    /api/v1/projects/{id}          # Get project details
PUT    /api/v1/projects/{id}          # Update project
DELETE /api/v1/projects/{id}          # Delete project
```

### 5.3 Funnel Management

```
GET    /api/v1/funnels                # List funnels
POST   /api/v1/funnels                # Create funnel
GET    /api/v1/funnels/{id}           # Get funnel details
PUT    /api/v1/funnels/{id}           # Update funnel
DELETE /api/v1/funnels/{id}           # Delete funnel
```

### 5.4 Event Tracking (Public - API Key Authentication)

```
POST   /api/v1/track                  # Track single event
POST   /api/v1/track/batch            # Track multiple events
```

### 5.5 Analytics Endpoints

```
GET    /api/v1/analytics/funnel/{funnel_id}  # Get funnel analytics
       Query params: start_date, end_date
```

### 5.6 Tracking Code

```
GET    /api/v1/projects/{id}/tracking-code   # Get JS tracking snippet
```

---

## 6. Implementation Steps

### Phase 1: Project Setup (Week 1)

**Backend Setup**:
1. Initialize FastAPI project structure
2. Set up Docker and Docker Compose (simplified - no database containers)
3. Configure file system storage (local or volume mount)
4. Set up data directory structure (events/, metadata/, config/)
5. Configure environment variables (.env)
6. Basic project structure:
   ```
   backend/
   ├── app/
   │   ├── __init__.py
   │   ├── main.py
   │   ├── config.py
   │   ├── storage/
   │   │   ├── __init__.py
   │   │   ├── parquet_handler.py      # Parquet read/write operations
   │   │   ├── metadata_handler.py     # JSON metadata operations
   │   │   └── duckdb_query.py         # DuckDB query interface
   │   ├── api/
   │   │   ├── __init__.py
   │   │   ├── deps.py
   │   │   └── v1/
   │   │       ├── auth.py
   │   │       ├── projects.py
   │   │       ├── funnels.py
   │   │       ├── track.py
   │   │       └── analytics.py
   │   ├── core/
   │   │   ├── security.py
   │   │   └── config.py
   │   ├── schemas/
   │   │   ├── user.py
   │   │   ├── project.py
   │   │   ├── funnel.py
   │   │   └── event.py
   │   ├── services/
   │   │   ├── auth_service.py
   │   │   ├── project_service.py
   │   │   ├── funnel_service.py
   │   │   └── analytics_service.py    # DuckDB queries for analytics
   │   └── utils/
   │       ├── file_utils.py           # File path helpers
   │       └── date_utils.py           # Date partitioning helpers
   ├── data/                            # Data directory (volume mount)
   │   ├── events/
   │   ├── metadata/
   │   └── config/
   ├── tests/
   ├── requirements.txt
   ├── Dockerfile
   └── docker-compose.yml               # Simplified (no DB, optional Redis)
   ```

**Frontend Setup**:
1. Initialize React + TypeScript + Vite project
2. Set up Tailwind CSS and shadcn/ui
3. Configure routing
4. Set up API client (Axios)
5. Project structure:
   ```
   frontend/
   ├── src/
   │   ├── components/
   │   │   ├── ui/          # shadcn components
   │   │   ├── layout/
   │   │   ├── funnel/
   │   │   └── charts/
   │   ├── pages/
   │   │   ├── Login.tsx
   │   │   ├── Dashboard.tsx
   │   │   ├── Projects.tsx
   │   │   └── Funnels.tsx
   │   ├── store/
   │   │   ├── authStore.ts
   │   │   └── projectStore.ts
   │   ├── services/
   │   │   └── api.ts
   │   ├── hooks/
   │   ├── utils/
   │   ├── App.tsx
   │   └── main.tsx
   ├── package.json
   └── vite.config.ts
   ```

### Phase 2: Authentication & User Management (Week 2)

**Backend**:
- [ ] User registration/login endpoints
- [ ] JWT token generation and validation
- [ ] Password hashing (bcrypt)
- [ ] Organization creation (auto-create on registration)
- [ ] JSON metadata file operations (read/write users.json)
- [ ] File-based user storage service
- [ ] API middleware for authentication
- [ ] Atomic file writes (prevent corruption during concurrent writes)

**Frontend**:
- [ ] Login/Signup pages
- [ ] Auth store (Zustand)
- [ ] Protected route wrapper
- [ ] API client with auth headers
- [ ] Token refresh logic

### Phase 3: Project & Funnel Management (Week 3)

**Backend**:
- [ ] Project CRUD endpoints
- [ ] Funnel CRUD endpoints
- [ ] API key generation for projects (hashed storage)
- [ ] Funnel stage validation
- [ ] JSON metadata file operations (projects.json, funnels.json)
- [ ] File-based storage services (atomic writes)
- [ ] Permissions (org-based access control)
- [ ] Directory creation for new projects (events/project_{id}/)

**Frontend**:
- [ ] Project list/create/edit pages
- [ ] Funnel list/create/edit pages
- [ ] Funnel stage builder UI
- [ ] Form validation

### Phase 4: Event Tracking System (Week 4-5)

**Backend**:
- [ ] Event ingestion endpoint (public API)
- [ ] API key validation middleware (check projects.json)
- [ ] Event validation (Pydantic schema validation)
- [ ] Batch event processing (accumulate events, write in batches)
- [ ] Rate limiting (in-memory or simple file-based counter, optional Redis)
- [ ] CORS configuration
- [ ] Parquet file write operations (daily partitions)
  - Append events to daily Parquet file
  - Create new file if doesn't exist
  - Batch writes for performance (e.g., every 100 events or 1 minute)
- [ ] Event buffering (in-memory buffer, flush to Parquet periodically)
- [ ] Async file I/O (aiofiles or ThreadPoolExecutor)

**Frontend**:
- [ ] Tracking code generator UI
- [ ] Copy-to-clipboard functionality
- [ ] Installation instructions

**Tracking SDK** (JavaScript):
```javascript
// Simple tracking script to be embedded
(function() {
  const script = document.createElement('script');
  script.src = 'https://cdn.iafa.com/tracker.js';
  script.setAttribute('data-api-key', 'YOUR_API_KEY');
  document.head.appendChild(script);
})();
```

### Phase 5: Analytics Engine (Week 6-7)

**Backend**:
- [ ] DuckDB integration for querying Parquet files
- [ ] Funnel calculation logic using DuckDB SQL
  - Query Parquet files by date range and project
  - Count distinct users per stage
  - Calculate conversion rates
  - Calculate drop-off rates
  - Handle time windows (date ranges) - partition pruning
- [ ] Parquet file path generation (based on date range)
- [ ] Query optimization (partition pruning, column selection)
- [ ] Analytics API endpoint (query DuckDB, return results)
- [ ] Optional: Caching query results (in-memory or file-based)
- [ ] Async query execution (DuckDB queries can be slow on large files)

**DuckDB Query Example**:
```python
# Example funnel calculation with DuckDB
def calculate_funnel_metrics(funnel_id: str, start_date: str, end_date: str):
    # Get funnel definition from metadata
    funnel = load_funnel(funnel_id)
    
    # Build file paths for date range (partition pruning)
    parquet_paths = generate_parquet_paths(
        project_id=funnel['project_id'],
        start_date=start_date,
        end_date=end_date
    )
    
    # Query with DuckDB
    query = f"""
    SELECT 
        event_type,
        user_id,
        MIN(created_at) as first_occurrence
    FROM read_parquet({parquet_paths})
    WHERE event_type IN ({funnel['event_types']})
      AND created_at >= '{start_date}'
      AND created_at < '{end_date}'
    GROUP BY event_type, user_id
    """
    
    result = duckdb_conn.execute(query).fetchdf()
    # Process results to calculate funnel metrics
    return calculate_stage_metrics(result, funnel['stages'])
```

**Frontend**:
- [ ] Funnel chart component (using Recharts)
- [ ] Metrics display cards
- [ ] Date range picker
- [ ] Loading states (queries can take a few seconds)
- [ ] Error handling

### Phase 6: Dashboard UI (Week 8)

**Frontend**:
- [ ] Dashboard layout
- [ ] Funnel visualization
  - Funnel chart (bar/step chart)
  - Stage labels with percentages
  - Color coding (green/red for conversion/drop-off)
- [ ] Metrics cards
  - Overall conversion rate
  - Total users entering funnel
  - Users at each stage
- [ ] Date range selector
- [ ] Empty states
- [ ] Responsive design

### Phase 7: Testing & Bug Fixes (Week 9)

**Backend Testing**:
- [ ] Unit tests for services
- [ ] API endpoint tests
- [ ] Database model tests
- [ ] Worker task tests
- [ ] Target: 70%+ code coverage

**Frontend Testing**:
- [ ] Component unit tests
- [ ] Integration tests for key flows
- [ ] E2E tests for critical paths (optional for MVP)

**Bug Fixes**:
- [ ] Fix identified bugs
- [ ] Performance optimization
- [ ] Security audit

### Phase 8: Deployment & Documentation (Week 10)

**Deployment**:
- [ ] Production environment setup
- [ ] Environment configuration
- [ ] Database migrations (production)
- [ ] SSL certificate setup
- [ ] Domain configuration
- [ ] Monitoring setup (basic logging)

**Documentation**:
- [ ] API documentation (FastAPI auto-docs)
- [ ] User guide (tracking code installation)
- [ ] Developer README
- [ ] Deployment guide

---

## 7. Key Implementation Details

### 7.1 Funnel Calculation Algorithm (DuckDB + Parquet)

```python
import duckdb
import pandas as pd
from pathlib import Path

def calculate_funnel_metrics(funnel_id: str, start_date: str, end_date: str):
    """
    Calculate funnel metrics for a given date range using DuckDB on Parquet files.
    Returns dict with stage metrics.
    """
    # Load funnel definition from metadata
    funnel = load_funnel_from_json(funnel_id)
    project_id = funnel['project_id']
    stages = funnel['stages']  # Sorted by order
    
    # Generate Parquet file paths for date range (partition pruning)
    parquet_files = generate_parquet_file_paths(
        project_id=project_id,
        start_date=start_date,
        end_date=end_date
    )
    
    if not parquet_files:
        return []  # No data for date range
    
    # Connect to DuckDB
    conn = duckdb.connect()
    
    # Query events from Parquet files
    # Get all relevant events for the funnel stages
    event_types = [stage['event'] for stage in stages]
    event_types_str = "', '".join(event_types)
    
    # Build query with partition pruning
    query = f"""
    SELECT 
        user_id,
        event_type,
        created_at
    FROM read_parquet({parquet_files})
    WHERE event_type IN ('{event_types_str}')
      AND created_at >= '{start_date}'
      AND created_at < '{end_date}'
    ORDER BY user_id, created_at
    """
    
    # Execute query and load into pandas DataFrame
    df = conn.execute(query).df()
    
    if df.empty:
        return []
    
    # Group by user and calculate stage progression
    user_events = df.groupby('user_id')['event_type'].apply(list).to_dict()
    
    # Calculate users at each stage
    stage_counts = {}
    for i, stage in enumerate(stages):
        stage_event = stage['event']
        users_at_stage = set()
        
        for user_id, user_event_list in user_events.items():
            # Check if user reached this stage
            # User must have completed all previous stages in order
            reached_stage = True
            
            # Check previous stages were completed
            for prev_stage_idx in range(i):
                prev_event = stages[prev_stage_idx]['event']
                if prev_event not in user_event_list:
                    reached_stage = False
                    break
            
            # Check if current stage event exists and occurs after previous stages
            if reached_stage and stage_event in user_event_list:
                users_at_stage.add(user_id)
        
        stage_counts[stage['name']] = len(users_at_stage)
    
    # Calculate conversion rates and drop-offs
    metrics = []
    prev_count = None
    first_stage_count = stage_counts[stages[0]['name']] if stages else 0
    
    for stage_name, count in stage_counts.items():
        rate = (count / first_stage_count * 100) if first_stage_count > 0 else 0
        drop_off = ((prev_count - count) / prev_count * 100) if prev_count and prev_count > 0 else 0
        
        metrics.append({
            'stage': stage_name,
            'users': count,
            'conversion_rate': round(rate, 2),
            'drop_off_rate': round(drop_off, 2)
        })
        prev_count = count
    
    conn.close()
    return metrics

def generate_parquet_file_paths(project_id: str, start_date: str, end_date: str) -> list:
    """Generate list of Parquet file paths for date range."""
    from datetime import datetime, timedelta
    from pathlib import Path
    
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    
    files = []
    current = start
    
    while current < end:
        date_str = current.strftime('%Y-%m-%d')
        file_path = Path(f"data/events/project_{project_id}/{current.year}/{current.month:02d}/events_{date_str}.parquet")
        
        if file_path.exists():
            files.append(str(file_path.absolute()))
        
        current += timedelta(days=1)
    
    return files
```

### 7.2 Event Validation

```python
from pydantic import BaseModel, Field, validator

class EventSchema(BaseModel):
    event_type: str = Field(..., min_length=1, max_length=100)
    user_id: str = Field(..., min_length=1, max_length=255)
    session_id: Optional[str] = None
    properties: Optional[dict] = {}
    url: Optional[str] = None
    referrer: Optional[str] = None
    timestamp: Optional[datetime] = None  # Client timestamp
    
    @validator('properties')
    def validate_properties(cls, v):
        if not isinstance(v, dict):
            raise ValueError('Properties must be a dictionary')
        # Ensure JSON-serializable
        return v
```

### 7.3 Rate Limiting Strategy

- **Per API Key**: 1000 events/minute
- **Per IP**: 100 events/minute (fallback)
- **Implementation**: 
  - Simple in-memory dictionary for MVP (reset on restart)
  - Optional: Redis-based sliding window (if Redis available)
  - Alternative: File-based counter with TTL (simple file timestamps)

### 7.4 CORS Configuration

- Allow configured domains (from project settings)
- Support wildcard subdomains
- Credentials: true for authenticated requests

---

## 8. Development Environment Setup

### 8.1 Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Docker and Docker Compose (optional - simplified stack)
- Git
- File system access (local or mounted volume)

**Note**: No database or Redis required for MVP! (Optional Redis for advanced rate limiting)

### 8.2 Local Development Setup

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create data directories
mkdir -p data/events data/metadata data/config

# Optional: Start Redis for rate limiting (if using)
# docker run -d -p 6379:6379 redis:7

# Start development server
uvicorn app.main:app --reload --port 8000
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev  # Starts on port 5173
```

**Note**: No separate worker process needed for MVP! (Optional background tasks with asyncio)

### 8.3 Environment Variables

**Backend (.env)**:
```env
# Data storage
DATA_DIR=./data                    # Local data directory (or absolute path)
STORAGE_TYPE=local                 # 'local' or 's3' (future)

# Optional Redis (for rate limiting/caching)
REDIS_URL=redis://localhost:6379/0  # Optional - can omit for MVP
USE_REDIS=false                    # Set to true if using Redis

# Security
SECRET_KEY=your-secret-key-here    # Generate with: openssl rand -hex 32
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# API Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
ENVIRONMENT=development
API_HOST=0.0.0.0
API_PORT=8000

# Event Buffering
EVENT_BUFFER_SIZE=100              # Batch size before writing to Parquet
EVENT_FLUSH_INTERVAL=60            # Flush buffer every N seconds
```

**Frontend (.env)**:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

### 8.4 Docker Compose (Simplified - Optional)

```yaml
version: '3.8'

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data          # Mount data directory
      - ./backend:/app             # Mount code for hot reload
    environment:
      - DATA_DIR=/app/data
      - ENVIRONMENT=development
    env_file:
      - .env

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
    environment:
      - VITE_API_URL=http://localhost:8000/api/v1

  # Optional Redis (only if using)
  redis:
    image: redis:7
    ports:
      - "6379:6379"
    profiles:
      - redis
```

---

## 9. Testing Strategy

### 9.1 Backend Tests

**Structure**:
```
tests/
├── test_auth.py
├── test_projects.py
├── test_funnels.py
├── test_tracking.py
├── test_analytics.py
└── conftest.py  # Fixtures
```

**Example Test**:
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_track_event(client: AsyncClient, api_key: str):
    response = await client.post(
        "/api/v1/track",
        headers={"X-API-Key": api_key},
        json={
            "event_type": "page_view",
            "user_id": "user123",
            "url": "https://example.com/page"
        }
    )
    assert response.status_code == 200
```

### 9.2 Frontend Tests

**Structure**:
```
src/
├── components/
│   └── __tests__/
│       └── FunnelChart.test.tsx
└── pages/
    └── __tests__/
        └── Dashboard.test.tsx
```

**Example Test**:
```typescript
import { render, screen } from '@testing-library/react';
import { FunnelChart } from '../FunnelChart';

describe('FunnelChart', () => {
  it('renders funnel stages', () => {
    const stages = [
      { name: 'Stage 1', users: 1000 },
      { name: 'Stage 2', users: 500 }
    ];
    render(<FunnelChart stages={stages} />);
    expect(screen.getByText('Stage 1')).toBeInTheDocument();
  });
});
```

---

## 10. Security Considerations

### 10.1 API Security

- **Authentication**: JWT tokens (HTTP-only cookies for web, Bearer token for API)
- **API Keys**: Store hashed API keys in projects.json metadata file
- **Rate Limiting**: Prevent abuse (in-memory or file-based for MVP)
- **Input Validation**: Pydantic schemas for all inputs
- **File Path Injection**: Validate file paths, prevent directory traversal
- **Parquet Query Injection**: DuckDB handles SQL injection prevention (parameterized queries)
- **CORS**: Restricted to allowed domains

### 10.2 Data Security

- **Encryption**: Passwords hashed with bcrypt
- **Secrets**: Environment variables, never commit
- **File Permissions**: Restrict file system permissions (600 for metadata files)
- **File Locking**: Use file locks for atomic writes (prevent corruption)
- **HTTPS**: Required for production
- **Backup**: Regular backups of Parquet files and metadata (simple file copy for MVP)

### 10.3 Privacy

- **IP Anonymization**: Hash or truncate IP addresses
- **User Data**: Support anonymous users
- **Data Retention**: 90-day retention policy
- **GDPR**: Basic compliance (data export, deletion)

---

## 11. Performance Optimization

### 11.1 Parquet File Optimization

- **Columnar Storage**: Parquet is columnar (faster for analytics queries)
- **Compression**: Use Snappy or Gzip compression (balance speed vs size)
- **Partitioning**: Partition by project_id/year/month/date (partition pruning)
- **Row Groups**: Optimize row group size (~128MB) for query performance
- **Daily Files**: One Parquet file per day (smaller files, faster queries)

### 11.2 DuckDB Query Optimization

- **Partition Pruning**: Only read Parquet files for date range (DuckDB auto-detects)
- **Column Selection**: Only select needed columns (Parquet columnar format helps)
- **Query Caching**: Cache query results in memory (simple dict with TTL)
- **Connection Pooling**: Reuse DuckDB connections (thread-safe)
- **Query Timeout**: Set timeout for long-running queries

### 11.3 Event Ingestion Optimization

- **Buffering**: Accumulate events in memory, write in batches
- **Batch Writes**: Write to Parquet every N events (100-1000) or time interval (1-5 min)
- **Async I/O**: Use asyncio or ThreadPoolExecutor for non-blocking file writes
- **File Locking**: Use file locks to prevent concurrent write issues

### 11.4 Caching (Optional)

- **In-Memory Caching**:
  - Funnel metrics (TTL: 5-10 minutes)
  - API key validation (TTL: 1 minute)
  - User sessions (JWT tokens, no cache needed)
- **File-Based Cache**: Simple JSON cache files for metrics (optional)

### 11.5 Data Retention

- **Cleanup Job**: Daily job to delete Parquet files older than 90 days
- **Compression**: Compress old files before deletion (optional)
- **Archive**: Move old files to archive directory (optional)

---

## 12. Deployment Plan

### 12.1 Production Stack

- **Hosting**: DigitalOcean/AWS/GCP (any VPS or cloud provider)
- **Application**: Docker containers or standalone Python process
- **Storage**: File system (local disk) or cloud storage (S3, GCS) for Parquet files
- **Cache**: Optional - Redis (can skip for MVP, use in-memory)
- **Web Server**: Nginx (reverse proxy) or direct uvicorn/gunicorn
- **SSL**: Let's Encrypt
- **Process Manager**: systemd, supervisor, or PM2 (optional)

**Simplified MVP Stack**:
- Single VPS/server
- FastAPI app (uvicorn/gunicorn)
- Local file system for Parquet files
- Nginx for reverse proxy + SSL
- No database, no Redis (can add later)

### 12.2 Deployment Steps

1. **Infrastructure Setup**:
   - Provision VPS/server (1GB RAM minimum, 10GB disk for MVP)
   - Set up Docker (optional) or install Python directly
   - Create data directory: `mkdir -p /var/iafa/data/{events,metadata,config}`
   - Set file permissions: `chmod 600 /var/iafa/data/metadata/*`
   - Configure domain and DNS
   - Set up SSL certificate (Certbot + Let's Encrypt)

2. **Application Deployment**:
   - Clone repository
   - Create virtual environment: `python -m venv venv`
   - Install dependencies: `pip install -r requirements.txt`
   - Set up environment variables (.env file)
   - Create data directories and set permissions
   - Start application with process manager (systemd/supervisor) or Docker
   - **No migrations needed!** (file-based storage)

3. **Monitoring**:
   - Application logs: `/var/log/iafa/app.log`
   - Error tracking: Basic logging to file
   - Health check endpoint: `GET /health`
   - Disk space monitoring (Parquet files can grow)

4. **Backup Strategy**:
   - Daily backups of data directory (rsync or tar)
   - Backup Parquet files and metadata JSON files
   - Backup retention: 30 days
   - Cloud backup: Sync to S3/GCS (optional)

### 12.3 Sample requirements.txt

```txt
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Data Processing
duckdb==0.9.2
pyarrow==14.0.1
pandas==2.1.3

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# File Operations
aiofiles==23.2.1

# HTTP Client (for tests)
httpx==0.25.2

# Optional Redis (if using)
redis==5.0.1

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# Code Quality
black==23.11.0
isort==5.12.0
mypy==1.7.0
pylint==3.0.2

# Utilities
python-dotenv==1.0.0
```

### 12.4 Sample systemd Service File

```ini
[Unit]
Description=IAFA API Service
After=network.target

[Service]
Type=simple
User=iafa
WorkingDirectory=/opt/iafa/backend
Environment="PATH=/opt/iafa/backend/venv/bin"
ExecStart=/opt/iafa/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## 13. MVP Limitations & Future Improvements

### 13.1 Known Limitations

1. **Single Project**: One project per organization (MVP)
2. **Batch Processing**: Real-time updates not available (Parquet writes are batched)
3. **Limited Segmentation**: Basic filtering only
4. **No Export**: Can't export reports (future feature)
5. **No Alerts**: No notification system
6. **Scalability**: Designed for small-medium traffic (<1M events/day per project)
7. **File-Based Storage**: Not suitable for extremely high concurrency (better for moderate traffic)
8. **No ACID Transactions**: File-based storage doesn't guarantee ACID (acceptable for analytics)
9. **Query Performance**: DuckDB queries may be slower on very large datasets (consider partitioning)
10. **Single Server**: Not distributed (single point of failure for MVP)

### 13.2 Future Enhancements

- **Database Migration**: Migrate to PostgreSQL/ClickHouse for better scalability
- **Real-time Analytics**: Stream processing with Kafka or similar
- **Cloud Storage**: Support S3/GCS for Parquet files (object storage)
- **Advanced Segmentation**: Multi-dimensional filtering
- **Cohort Analysis**: User cohort tracking and analysis
- **Machine Learning**: Conversion prediction models
- **Export Functionality**: PDF/CSV report exports
- **Scheduled Reports**: Automated report generation and email delivery
- **Email Notifications**: Alert system for funnel drops
- **Multi-project Support**: Multiple projects per organization
- **API Webhooks**: Event webhooks for integrations
- **Mobile App Tracking SDK**: iOS/Android SDKs
- **Distributed Processing**: Spark or similar for large-scale analytics
- **Query Optimization**: Materialized views or pre-aggregated metrics

---

## 14. Success Criteria for MVP

### Technical Criteria

- ✅ All core features implemented
- ✅ API response time < 200ms (95th percentile)
- ✅ Dashboard load time < 2 seconds
- ✅ Support 10,000 events/day per project
- ✅ 99% uptime target
- ✅ Code coverage > 70%

### Functional Criteria

- ✅ Users can create projects and funnels
- ✅ Tracking code can be integrated in < 5 minutes
- ✅ Funnel visualization is accurate
- ✅ Date filtering works correctly
- ✅ Authentication is secure

---

## 15. Risk Mitigation

### Technical Risks

1. **Database Performance**
   - *Risk*: Events table grows too large
   - *Mitigation*: Aggregation strategy, data retention, indexing

2. **Scalability**
   - *Risk*: High event volume overwhelms system
   - *Mitigation*: Queue-based processing, rate limiting, horizontal scaling (future)

3. **Data Accuracy**
   - *Risk*: Funnel calculations may be incorrect
   - *Mitigation*: Thorough testing, validation, edge case handling

### Business Risks

1. **User Adoption**
   - *Risk*: Complex setup deters users
   - *Mitigation*: Simple tracking code, clear documentation, onboarding

2. **Feature Gaps**
   - *Risk*: Missing critical features vs competitors
   - *Mitigation*: Focus on core value, gather user feedback, iterate

---

## Appendix

### A. API Response Examples

**Funnel Analytics Response**:
```json
{
  "funnel_id": "uuid",
  "name": "E-commerce Funnel",
  "date_range": {
    "start": "2024-01-01",
    "end": "2024-01-31"
  },
  "stages": [
    {
      "stage_name": "Page View",
      "order": 1,
      "users": 10000,
      "conversion_rate": 100.0,
      "drop_off_rate": 0.0
    },
    {
      "stage_name": "Add to Cart",
      "order": 2,
      "users": 3000,
      "conversion_rate": 30.0,
      "drop_off_rate": 70.0
    },
    {
      "stage_name": "Purchase",
      "order": 3,
      "users": 1500,
      "conversion_rate": 15.0,
      "drop_off_rate": 50.0
    }
  ],
  "overall_conversion_rate": 15.0
}
```

### B. Tracking Code Example

**Generated JavaScript**:
```javascript
(function() {
  const _iafa = window._iafa || [];
  const apiKey = 'YOUR_API_KEY';
  const apiUrl = 'https://api.iafa.com/api/v1/track';
  
  function track(eventType, properties = {}) {
    const payload = {
      event_type: eventType,
      user_id: _iafa.userId || getUserId(),
      session_id: _iafa.sessionId || getSessionId(),
      properties: properties,
      url: window.location.href,
      referrer: document.referrer,
      timestamp: new Date().toISOString()
    };
    
    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey
      },
      body: JSON.stringify(payload)
    }).catch(console.error);
  }
  
  // Auto-track page views
  track('page_view');
  
  // Expose public API
  window._iafa = { track, userId: null, sessionId: null };
})();
```

---

**Document Status**: Ready for Implementation (Parquet-based MVP)  
**Next Steps**: Begin Phase 1 - Project Setup  
**Estimated Completion**: 6-8 weeks from start date (reduced timeline due to simplified file-based storage)

---

## Summary of Parquet-Based Architecture Benefits

### Advantages for MVP:
1. **Simpler Setup**: No database installation or management required
2. **Faster Development**: No ORM, migrations, or database schema to maintain
3. **Lower Infrastructure Cost**: No database server needed (VPS only)
4. **Easier Deployment**: Single application container, simple file storage
5. **Better Analytics Performance**: Columnar Parquet format optimized for analytics queries
6. **Scalable to Cloud**: Easy migration to S3/GCS later
7. **No Database Connection Issues**: File-based access, no connection pooling needed
8. **Simpler Backup**: Just copy files (rsync, tar, cloud sync)

### Trade-offs:
1. **Concurrency Limits**: File-based storage has lower write concurrency than databases
2. **No ACID**: File writes don't guarantee ACID properties (acceptable for analytics)
3. **Query Performance**: DuckDB is fast but not as optimized as dedicated analytics DBs for very large datasets
4. **File Management**: Need to manage file cleanup, partitioning, and organization manually

### When to Migrate to Database:
- Need >10M events/day per project
- Require ACID transactions
- Need distributed/multi-server architecture
- Require complex joins across entities
- Need real-time analytics with <1s latency
