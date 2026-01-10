# Data Strategy & Architecture

## Data Philosophy

**Core Principles**:
1. **Privacy-First**: User data is private by default, no third-party sharing
2. **Columnar Storage**: Parquet format for optimal analytics performance
3. **Partition-Based**: Date-based partitioning for efficient queries
4. **Schema Evolution**: Flexible schema to accommodate future changes
5. **Data Retention**: 90-day retention for raw events (MVP)

## Data Architecture Overview

### Storage Layer

```
┌─────────────────────────────────────────┐
│         Event Data (Parquet)            │
│  Partitioned by: project_id/date        │
│  Schema: Optimized for analytics        │
│  Retention: 90 days                     │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      Metadata (JSON Files)              │
│  - Users, Projects, Funnels             │
│  - Configuration, Settings              │
│  - Retention: Indefinite                │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│       Query Engine (DuckDB)             │
│  - Embedded analytics database          │
│  - SQL queries on Parquet files         │
│  - In-memory processing                 │
└─────────────────────────────────────────┘
```

## Data Flow

### Event Ingestion Flow

```
1. Client (Browser/Mobile) → Tracking SDK
2. SDK → FastAPI /api/v1/track endpoint
3. FastAPI → Event Validation (Pydantic)
4. FastAPI → Event Buffer (In-Memory)
5. Buffer → Batch Write to Parquet (every N events or time interval)
6. Parquet File → data/events/project_{id}/{year}/{month}/events_{date}.parquet
```

### Analytics Query Flow

```
1. User → Dashboard UI (select funnel, date range)
2. UI → FastAPI /api/v1/analytics/funnel/{id} endpoint
3. FastAPI → Load Funnel Definition (metadata/funnels.json)
4. FastAPI → Generate Parquet File Paths (partition pruning)
5. FastAPI → DuckDB Query (SQL on Parquet files)
6. DuckDB → Execute Query (columnar scan)
7. DuckDB → Return Results (DataFrame)
8. FastAPI → Process Results (calculate metrics)
9. FastAPI → Return JSON to UI
10. UI → Display Funnel Visualization
```

## Data Storage Strategy

### Event Data (Parquet)

**File Structure**:
```
data/events/
└── project_{project_id}/
    └── {year}/
        └── {month}/
            └── events_{YYYY-MM-DD}.parquet
```

**Partitioning Strategy**:
- **Primary Partition**: `project_id` (data isolation)
- **Secondary Partition**: `year` (temporal organization)
- **Tertiary Partition**: `month` (query optimization)
- **File Level**: Daily files (balance between file count and size)

**Benefits**:
- **Partition Pruning**: DuckDB only reads relevant files
- **Parallel Queries**: Can query multiple files simultaneously
- **Efficient Cleanup**: Delete old files by date easily
- **Scalability**: Add new partitions as data grows

**File Size Targets**:
- Target: 10-50MB per daily file (optimized for query performance)
- Max: 100MB per file (split if exceeded)
- Min: 1MB per file (merge small files if needed)

### Metadata (JSON)

**File Structure**:
```
data/metadata/
├── users.json          # User accounts
├── projects.json       # Project configurations
└── funnels.json        # Funnel definitions
```

**Storage Strategy**:
- **Atomic Writes**: Write to temp file, then rename (prevent corruption)
- **File Locking**: Prevent concurrent write issues
- **Backup**: Daily backups of metadata files
- **Versioning**: Keep last N versions for rollback

## Data Schema

### Event Schema (Parquet)

```python
{
    "id": "string",              # UUID v4
    "project_id": "string",      # Project identifier
    "event_type": "string",      # Event type (e.g., "page_view", "purchase")
    "user_id": "string",         # User identifier (anonymous or authenticated)
    "session_id": "string",      # Session identifier
    "properties": {              # Event properties (key-value pairs)
        "key1": "value1",
        "key2": "value2"
    },
    "url": "string",             # Page URL (max 500 chars)
    "referrer": "string",        # Referrer URL (max 500 chars)
    "user_agent": "string",      # User agent string
    "ip_address": "string",      # IP address (hashed for privacy)
    "device_type": "string",     # "desktop", "mobile", "tablet"
    "browser": "string",         # Browser name
    "os": "string",              # Operating system
    "country": "string",         # Country code (ISO 3166-1 alpha-2)
    "created_at": "timestamp",   # Event timestamp (UTC)
    "client_timestamp": "timestamp"  # Client-side timestamp (if available)
}
```

**Parquet File Properties**:
- Compression: Snappy (good balance of speed and compression)
- Row Group Size: 128MB (optimized for analytics queries)
- Column Encoding: Dictionary encoding for categorical columns
- Statistics: Min/max statistics for efficient filtering

### Funnel Schema (JSON)

```json
{
    "id": "uuid",
    "project_id": "uuid",
    "name": "E-commerce Purchase Funnel",
    "description": "Track users from page view to purchase",
    "stages": [
        {
            "order": 1,
            "name": "Page View",
            "event_type": "page_view",
            "filter": null  // Optional: additional filters
        },
        {
            "order": 2,
            "name": "Add to Cart",
            "event_type": "add_to_cart",
            "filter": null
        },
        {
            "order": 3,
            "name": "Checkout Started",
            "event_type": "checkout_started",
            "filter": null
        },
        {
            "order": 4,
            "name": "Purchase Completed",
            "event_type": "purchase",
            "filter": {
                "properties.status": "completed"
            }
        }
    ],
    "is_active": true,
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
}
```

## Data Quality & Validation

### Event Validation Rules

1. **Required Fields**: `event_type`, `user_id`, `project_id`, `created_at`
2. **Field Types**: Validate data types (string, timestamp, etc.)
3. **Field Lengths**: Enforce max lengths (URL: 500 chars, etc.)
4. **Timestamp Validation**: Ensure timestamps are within reasonable range
5. **User ID Format**: Validate user ID format (UUID or custom format)
6. **Event Type**: Whitelist or regex validation for event types

### Data Cleaning

1. **Duplicate Detection**: Remove duplicate events (same id)
2. **Timestamp Correction**: Handle client/server clock skew
3. **IP Anonymization**: Hash IP addresses for privacy
4. **Invalid Data**: Reject invalid events, log for analysis
5. **Sanitization**: Clean user input (prevent injection attacks)

### Data Quality Metrics

- **Event Capture Rate**: % of expected events captured
- **Data Accuracy**: % of events with valid data
- **Duplicate Rate**: % of duplicate events
- **Missing Data Rate**: % of events with missing required fields

## Query Optimization Strategy

### DuckDB Query Patterns

**Funnel Calculation Query**:
```sql
-- Example: Get users who completed each stage
WITH user_events AS (
    SELECT 
        user_id,
        event_type,
        MIN(created_at) as first_occurrence
    FROM read_parquet(['file1.parquet', 'file2.parquet', ...])
    WHERE created_at >= '2024-01-15'
      AND created_at < '2024-01-16'
      AND event_type IN ('page_view', 'add_to_cart', 'purchase')
    GROUP BY user_id, event_type
)
SELECT 
    event_type,
    COUNT(DISTINCT user_id) as unique_users
FROM user_events
GROUP BY event_type
ORDER BY event_type;
```

**Optimization Techniques**:
1. **Partition Pruning**: Only read files for date range
2. **Column Selection**: Only select needed columns
3. **Predicate Pushdown**: Filter early in query
4. **Statistics**: Use min/max statistics for filtering
5. **Caching**: Cache query results in memory (TTL: 5-10 minutes)

## Data Retention & Cleanup

### Retention Policy

- **Raw Events**: 90 days (configurable)
- **Metadata**: Indefinite (users, projects, funnels)
- **Aggregated Metrics**: Indefinite (future feature)

### Cleanup Strategy

**Daily Cleanup Job**:
```python
def cleanup_old_events():
    cutoff_date = datetime.now() - timedelta(days=90)
    
    # Find all Parquet files older than cutoff
    old_files = find_parquet_files_before(cutoff_date)
    
    # Delete old files
    for file_path in old_files:
        if file_path.exists():
            file_path.unlink()
            log.info(f"Deleted old file: {file_path}")
```

**Backup Before Cleanup**:
- Archive old files to cold storage (optional)
- Compress old files before deletion
- Keep metadata about deleted files

## Data Privacy & Compliance

### GDPR Compliance

- **Right to Access**: Users can request their data
- **Right to Deletion**: Users can delete their data
- **Data Minimization**: Only collect necessary data
- **Purpose Limitation**: Use data only for stated purpose
- **Storage Limitation**: 90-day retention policy

### Data Anonymization

- **IP Addresses**: Hash IP addresses (SHA-256)
- **User IDs**: Support anonymous user IDs
- **User Agent**: Can be truncated for privacy
- **URLs**: Remove query parameters if sensitive

### Data Security

- **Encryption at Rest**: Encrypt Parquet files (optional)
- **Encryption in Transit**: HTTPS for all API calls
- **Access Control**: File permissions (600 for metadata)
- **Audit Logging**: Log all data access (future feature)

---

**Document Owner**: Data Science Team  
**Last Updated**: Current Date  
**Status**: ✅ Complete
