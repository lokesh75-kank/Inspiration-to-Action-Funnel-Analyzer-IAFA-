# System Architecture

## Architecture Overview

IAFA MVP uses a **simplified file-based architecture** with Parquet files for event storage and DuckDB for analytics queries. This approach eliminates the need for a traditional database while maintaining excellent analytics performance.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Web Browser  │  │ Mobile Web   │  │ External API │      │
│  │ (Dashboard)  │  │ (Future)     │  │ (Future)     │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼──────────────┘
          │                  │                  │
          │ HTTPS            │ HTTPS            │ HTTPS
          │                  │                  │
┌─────────▼──────────────────▼──────────────────▼──────────────┐
│                      API Gateway Layer                        │
│                    FastAPI Application                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Authentication & Authorization                       │   │
│  │  - JWT token validation                              │   │
│  │  - API key validation                                │   │
│  │  - Rate limiting                                     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Endpoints                                        │   │
│  │  - /api/v1/auth/*       (Authentication)             │   │
│  │  - /api/v1/projects/*   (Project Management)         │   │
│  │  - /api/v1/funnels/*    (Funnel Management)          │   │
│  │  - /api/v1/track        (Event Tracking)             │   │
│  │  - /api/v1/analytics/*  (Analytics Queries)          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────┬────────────────────────────────────────────────────┘
          │
          │
┌─────────▼────────────────────────────────────────────────────┐
│                    Application Layer                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │  Auth Service   │  │  Project Service│  │ Event Service│ │
│  │  - User mgmt    │  │  - CRUD ops     │  │ - Validation │ │
│  │  - JWT tokens   │  │  - API keys     │  │ - Buffering  │ │
│  └─────────────────┘  └─────────────────┘  └──────┬───────┘ │
│  ┌─────────────────┐  ┌─────────────────┐         │         │
│  │ Funnel Service  │  │ Analytics       │         │         │
│  │ - CRUD ops      │  │ Service         │         │         │
│  │ - Validation    │  │ - DuckDB queries│         │         │
│  └─────────────────┘  └─────────────────┘         │         │
└─────────┬──────────────────────────────┬───────────┼─────────┘
          │                              │           │
          │                              │           │
┌─────────▼──────────┐     ┌────────────▼───┐  ┌────▼──────────┐
│  Storage Layer     │     │  Query Engine  │  │  Optional     │
│  ┌──────────────┐  │     │  ┌──────────┐  │  │  ┌──────────┐ │
│  │ Parquet      │  │     │  │  DuckDB  │  │  │  │  Redis   │ │
│  │ Files        │  │     │  │  (Embed) │  │  │  │  (Cache) │ │
│  │ - Events     │  │     │  │  - SQL   │  │  │  │  - Rate  │ │
│  │ - Partitioned│  │     │  │  - Fast  │  │  │  │  limit   │ │
│  └──────────────┘  │     │  └──────────┘  │  │  └──────────┘ │
│  ┌──────────────┐  │     └────────────────┘  └───────────────┘
│  │ JSON Metadata│  │
│  │ - Users      │  │
│  │ - Projects   │  │
│  │ - Funnels    │  │
│  └──────────────┘  │
└────────────────────┘
```

## Component Architecture

### 1. API Gateway (FastAPI)

**Responsibilities**:
- HTTP request handling
- Authentication & authorization
- Request validation (Pydantic schemas)
- Rate limiting
- Error handling
- CORS configuration

**Technology**: FastAPI, Uvicorn

### 2. Application Services

#### Auth Service
- User registration/login
- JWT token generation/validation
- Password hashing (bcrypt)
- File-based user storage (JSON)

#### Project Service
- Project CRUD operations
- API key generation (hashed)
- File-based project storage (JSON)

#### Funnel Service
- Funnel CRUD operations
- Stage validation
- File-based funnel storage (JSON)

#### Event Service
- Event validation (Pydantic)
- Event buffering (in-memory)
- Batch writes to Parquet
- Async file I/O

#### Analytics Service
- Funnel calculation logic
- DuckDB query generation
- Result processing
- Metric calculations

### 3. Storage Layer

#### Parquet Files (Event Storage)

**Directory Structure**:
```
data/events/
└── project_{project_id}/
    └── {year}/
        └── {month}/
            └── events_{YYYY-MM-DD}.parquet
```

**Properties**:
- Columnar format (optimized for analytics)
- Snappy compression
- Partitioned by project_id/date
- Daily files (10-50MB each)

**Operations**:
- **Write**: Batch append (accumulate events, write periodically)
- **Read**: DuckDB queries (SQL on Parquet)
- **Delete**: Old file cleanup (90-day retention)

#### JSON Metadata Files

**Files**:
- `metadata/users.json` - User accounts
- `metadata/projects.json` - Project configurations
- `metadata/funnels.json` - Funnel definitions

**Operations**:
- **Read**: Load into memory on startup, cache
- **Write**: Atomic writes (temp file + rename)
- **Locking**: File locks for concurrent access

### 4. Query Engine (DuckDB)

**Purpose**: Embedded analytics database for querying Parquet files

**Features**:
- SQL queries on Parquet files
- Automatic partition pruning
- Columnar query execution
- In-memory processing
- No separate database process needed

**Usage**:
```python
import duckdb

conn = duckdb.connect()
result = conn.execute("""
    SELECT event_type, COUNT(*) 
    FROM read_parquet(['file1.parquet', 'file2.parquet'])
    WHERE created_at >= '2024-01-15'
    GROUP BY event_type
""").fetchdf()
```

### 5. Optional: Redis Cache (Future)

**Purpose**: Rate limiting, query result caching

**Usage** (if implemented):
- API key validation cache (TTL: 5 min)
- Query result cache (TTL: 10 min)
- Rate limiting counters (sliding window)

## Data Flow

### Event Ingestion Flow

```
1. Client SDK → POST /api/v1/track
   - Headers: X-API-Key
   - Body: {event_type, user_id, properties, ...}

2. FastAPI → Authentication Middleware
   - Validate API key (check projects.json)
   - Rate limiting check

3. FastAPI → Event Validation
   - Pydantic schema validation
   - Field type/length validation

4. FastAPI → Event Service
   - Add to in-memory buffer
   - If buffer size >= threshold (100 events) OR
     time interval elapsed (60 seconds):
     → Batch write to Parquet file

5. Parquet Writer → Async File I/O
   - Generate file path (project_id/date)
   - Append events to Parquet file
   - Create new file if doesn't exist
   - Use file locks for concurrent writes

6. Response → 200 OK (event accepted)
```

### Analytics Query Flow

```
1. Dashboard UI → GET /api/v1/analytics/funnel/{id}
   - Query params: start_date, end_date
   - Headers: Authorization (JWT)

2. FastAPI → Authentication
   - Validate JWT token
   - Check user permissions

3. FastAPI → Load Funnel Definition
   - Read metadata/funnels.json
   - Find funnel by ID
   - Validate funnel belongs to user's organization

4. FastAPI → Generate Parquet File Paths
   - Date range: start_date to end_date
   - Project ID: funnel.project_id
   - Generate list of Parquet file paths (partition pruning)

5. FastAPI → Analytics Service
   - Build DuckDB SQL query
   - Query Parquet files
   - Filter by event types (funnel stages)
   - Group by user_id, event_type
   - Calculate sequential progression

6. DuckDB → Execute Query
   - Read Parquet files (columnar scan)
   - Apply filters (partition pruning)
   - Aggregate results
   - Return DataFrame

7. Analytics Service → Process Results
   - Calculate stage counts
   - Calculate conversion rates
   - Calculate drop-off rates
   - Format response

8. FastAPI → Return JSON
   {
     "funnel_id": "...",
     "date_range": {...},
     "stages": [
       {"stage_name": "...", "users": 1000, "conversion_rate": 100.0},
       ...
     ]
   }

9. Dashboard UI → Render Visualization
   - Funnel chart (Recharts)
   - Metrics cards
```

## Technology Stack Summary

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **Data Storage**: Parquet files (PyArrow)
- **Query Engine**: DuckDB 0.9+
- **Authentication**: JWT (python-jose), bcrypt (passlib)
- **Validation**: Pydantic 2.5+
- **Async I/O**: aiofiles 23.2+
- **Optional**: Redis 5.0+ (rate limiting/caching)

### Frontend
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **State Management**: Zustand
- **UI Library**: Tailwind CSS + shadcn/ui
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Routing**: React Router v6

### Infrastructure (MVP)
- **Hosting**: VPS (DigitalOcean/AWS Lightsail)
- **Storage**: Local file system
- **Web Server**: Nginx (reverse proxy) or direct Uvicorn
- **Process Manager**: systemd, supervisor, or PM2
- **SSL**: Let's Encrypt

## Scalability Considerations

### Current Limits (MVP)
- **Events per day**: 10,000-100,000 per project
- **Concurrent users**: 100-500
- **Query performance**: < 2 seconds for 90-day range
- **Storage**: Local disk (10GB-100GB)

### Scaling Path (Post-MVP)
1. **Cloud Storage**: Migrate Parquet files to S3/GCS
2. **Database Migration**: PostgreSQL/ClickHouse for scale
3. **Distributed Processing**: Spark or similar
4. **Caching Layer**: Redis for query results
5. **Load Balancing**: Multiple API servers
6. **CDN**: Static assets caching

## Security Architecture

### Authentication
- **JWT Tokens**: Stateless authentication
- **API Keys**: Hashed storage in projects.json
- **Password Hashing**: bcrypt (cost factor: 12)

### Authorization
- **Organization-based**: Users access only their org's data
- **Project-level**: API keys scoped to projects
- **Funnel-level**: Users can only access their org's funnels

### Data Security
- **File Permissions**: 600 for metadata files
- **Path Validation**: Prevent directory traversal
- **Input Validation**: Pydantic schemas
- **SQL Injection**: DuckDB uses parameterized queries
- **HTTPS**: Required for production

### Privacy
- **IP Anonymization**: Hash IP addresses
- **Data Retention**: 90-day policy
- **GDPR Compliance**: Right to access/deletion
- **No Third-Party Sharing**: Data stays private

---

**Document Owner**: Development Team  
**Last Updated**: Current Date  
**Status**: ✅ Complete
