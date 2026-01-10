# API Design & Specifications

## API Overview

**Base URL**: `https://api.iafa.com/api/v1` (production)  
**Base URL**: `http://localhost:8000/api/v1` (development)  
**Version**: v1  
**Format**: JSON  
**Authentication**: JWT Bearer tokens (user endpoints) or API Keys (tracking endpoints)

## Authentication

### JWT Authentication (User Endpoints)

**Header**: `Authorization: Bearer {jwt_token}`

**Token Expiration**: 24 hours  
**Refresh Token**: Not implemented in MVP (can extend later)

### API Key Authentication (Tracking Endpoints)

**Header**: `X-API-Key: {api_key}`

**API Key Format**: Base64-encoded string (64 characters)  
**API Key Generation**: Secure random string, hashed before storage

## API Endpoints

### 1. Authentication Endpoints

#### POST `/api/v1/auth/register`

Register a new user account.

**Request**:
```json
{
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "full_name": "John Doe"
}
```

**Response** (201 Created):
```json
{
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "organization_id": "uuid",
    "created_at": "2024-01-15T10:00:00Z"
}
```

**Errors**:
- `400 Bad Request`: Invalid email format, weak password
- `409 Conflict`: Email already exists

---

#### POST `/api/v1/auth/login`

Login with email and password.

**Request**:
```json
{
    "email": "user@example.com",
    "password": "SecurePassword123!"
}
```

**Response** (200 OK):
```json
{
    "access_token": "jwt_token_here",
    "token_type": "bearer",
    "expires_in": 86400,
    "user": {
        "id": "uuid",
        "email": "user@example.com",
        "full_name": "John Doe",
        "organization_id": "uuid"
    }
}
```

**Errors**:
- `401 Unauthorized`: Invalid credentials

---

#### GET `/api/v1/auth/me`

Get current authenticated user information.

**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
{
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "organization_id": "uuid",
    "role": "owner",
    "created_at": "2024-01-15T10:00:00Z"
}
```

---

### 2. Project Management Endpoints

#### GET `/api/v1/projects`

List all projects for the authenticated user's organization.

**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
{
    "projects": [
        {
            "id": "uuid",
            "name": "My Project",
            "api_key": "masked_key_***",
            "domain": "example.com",
            "created_at": "2024-01-15T10:00:00Z"
        }
    ]
}
```

---

#### POST `/api/v1/projects`

Create a new project.

**Headers**: `Authorization: Bearer {token}`

**Request**:
```json
{
    "name": "My New Project",
    "domain": "example.com"
}
```

**Response** (201 Created):
```json
{
    "id": "uuid",
    "name": "My New Project",
    "api_key": "full_api_key_here",
    "domain": "example.com",
    "created_at": "2024-01-15T10:00:00Z"
}
```

**Note**: API key is returned only once on creation. Store it securely.

---

#### GET `/api/v1/projects/{project_id}`

Get project details.

**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
{
    "id": "uuid",
    "name": "My Project",
    "api_key": "masked_key_***",
    "domain": "example.com",
    "created_at": "2024-01-15T10:00:00Z"
}
```

---

#### PUT `/api/v1/projects/{project_id}`

Update project settings.

**Headers**: `Authorization: Bearer {token}`

**Request**:
```json
{
    "name": "Updated Project Name",
    "domain": "newdomain.com"
}
```

**Response** (200 OK):
```json
{
    "id": "uuid",
    "name": "Updated Project Name",
    "api_key": "masked_key_***",
    "domain": "newdomain.com",
    "updated_at": "2024-01-15T11:00:00Z"
}
```

---

#### DELETE `/api/v1/projects/{project_id}`

Delete a project (and all associated data).

**Headers**: `Authorization: Bearer {token}`

**Response** (204 No Content)

**Warning**: This action cannot be undone. All events and funnels will be deleted.

---

### 3. Funnel Management Endpoints

#### GET `/api/v1/funnels`

List all funnels for the authenticated user's organization.

**Headers**: `Authorization: Bearer {token}`  
**Query Params**: `?project_id={uuid}` (optional, filter by project)

**Response** (200 OK):
```json
{
    "funnels": [
        {
            "id": "uuid",
            "project_id": "uuid",
            "name": "E-commerce Purchase Funnel",
            "description": "Track users from page view to purchase",
            "stages": [
                {
                    "order": 1,
                    "name": "Page View",
                    "event_type": "page_view"
                },
                {
                    "order": 2,
                    "name": "Add to Cart",
                    "event_type": "add_to_cart"
                },
                {
                    "order": 3,
                    "name": "Purchase",
                    "event_type": "purchase"
                }
            ],
            "is_active": true,
            "created_at": "2024-01-15T10:00:00Z"
        }
    ]
}
```

---

#### POST `/api/v1/funnels`

Create a new funnel.

**Headers**: `Authorization: Bearer {token}`

**Request**:
```json
{
    "project_id": "uuid",
    "name": "My Funnel",
    "description": "Track user journey",
    "stages": [
        {
            "order": 1,
            "name": "Stage 1",
            "event_type": "page_view"
        },
        {
            "order": 2,
            "name": "Stage 2",
            "event_type": "click"
        }
    ]
}
```

**Response** (201 Created):
```json
{
    "id": "uuid",
    "project_id": "uuid",
    "name": "My Funnel",
    "description": "Track user journey",
    "stages": [...],
    "is_active": true,
    "created_at": "2024-01-15T10:00:00Z"
}
```

**Validation**:
- Max 5 stages (MVP limitation)
- Stages must have unique orders (1, 2, 3, ...)
- Event types must be valid strings

---

#### GET `/api/v1/funnels/{funnel_id}`

Get funnel details.

**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK): Same as POST response

---

#### PUT `/api/v1/funnels/{funnel_id}`

Update funnel definition.

**Headers**: `Authorization: Bearer {token}`

**Request**: Same as POST request

**Response** (200 OK): Updated funnel object

---

#### DELETE `/api/v1/funnels/{funnel_id}`

Delete a funnel.

**Headers**: `Authorization: Bearer {token}`

**Response** (204 No Content)

---

### 4. Event Tracking Endpoints (Public API)

#### POST `/api/v1/track`

Track a single event.

**Headers**: `X-API-Key: {api_key}`

**Request**:
```json
{
    "event_type": "page_view",
    "user_id": "user_123",
    "session_id": "session_456",
    "properties": {
        "url": "https://example.com/page",
        "title": "Page Title"
    },
    "url": "https://example.com/page",
    "referrer": "https://google.com",
    "user_agent": "Mozilla/5.0...",
    "timestamp": "2024-01-15T10:00:00Z"
}
```

**Response** (200 OK):
```json
{
    "success": true,
    "event_id": "uuid",
    "message": "Event tracked successfully"
}
```

**Note**: `timestamp` is optional (server timestamp used if not provided)

---

#### POST `/api/v1/track/batch`

Track multiple events in a single request.

**Headers**: `X-API-Key: {api_key}`

**Request**:
```json
{
    "events": [
        {
            "event_type": "page_view",
            "user_id": "user_123",
            ...
        },
        {
            "event_type": "click",
            "user_id": "user_123",
            ...
        }
    ]
}
```

**Response** (200 OK):
```json
{
    "success": true,
    "events_processed": 2,
    "event_ids": ["uuid1", "uuid2"]
}
```

**Rate Limiting**: 1000 events/minute per API key

---

### 5. Analytics Endpoints

#### GET `/api/v1/analytics/funnel/{funnel_id}`

Get funnel analytics for a date range.

**Headers**: `Authorization: Bearer {token}`

**Query Params**:
- `start_date` (required): ISO 8601 date (e.g., `2024-01-15`)
- `end_date` (required): ISO 8601 date (e.g., `2024-01-31`)
- `timezone` (optional): Timezone (default: UTC)

**Response** (200 OK):
```json
{
    "funnel_id": "uuid",
    "funnel_name": "E-commerce Purchase Funnel",
    "date_range": {
        "start": "2024-01-15",
        "end": "2024-01-31"
    },
    "stages": [
        {
            "stage_name": "Page View",
            "stage_order": 1,
            "users": 10000,
            "conversion_rate": 100.0,
            "drop_off_rate": 0.0
        },
        {
            "stage_name": "Add to Cart",
            "stage_order": 2,
            "users": 3000,
            "conversion_rate": 30.0,
            "drop_off_rate": 70.0
        },
        {
            "stage_name": "Purchase",
            "stage_order": 3,
            "users": 1500,
            "conversion_rate": 15.0,
            "drop_off_rate": 50.0
        }
    ],
    "overall_conversion_rate": 15.0,
    "total_users": 10000,
    "completed_users": 1500
}
```

**Errors**:
- `400 Bad Request`: Invalid date range (end_date < start_date, range > 90 days)
- `404 Not Found`: Funnel not found
- `500 Internal Server Error`: Query failed (check logs)

---

#### GET `/api/v1/projects/{project_id}/tracking-code`

Get JavaScript tracking code snippet for a project.

**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
{
    "tracking_code": "<script>...tracking code...</script>",
    "api_key": "masked_key_***",
    "instructions": "Copy and paste this code before </body> tag"
}
```

---

## Error Responses

### Standard Error Format

```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error message",
        "details": {
            "field": "Additional error details (optional)"
        }
    }
}
```

### Common Error Codes

- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists
- `422 Unprocessable Entity`: Validation errors
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Example Error Response

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Validation failed",
        "details": {
            "email": "Invalid email format",
            "password": "Password must be at least 8 characters"
        }
    }
}
```

## Rate Limiting

### Limits (MVP)

- **Authentication Endpoints**: 10 requests/minute per IP
- **Project/Funnel Endpoints**: 60 requests/minute per user
- **Analytics Endpoints**: 30 requests/minute per user
- **Tracking Endpoints**: 1000 events/minute per API key

### Rate Limit Headers

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1642233600
```

### Rate Limit Exceeded Response

**Status**: 429 Too Many Requests

```json
{
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Rate limit exceeded. Please try again later.",
        "retry_after": 60
    }
}
```

## CORS Configuration

**Allowed Origins**: Configurable per project (domain settings)  
**Allowed Methods**: GET, POST, PUT, DELETE, OPTIONS  
**Allowed Headers**: Authorization, X-API-Key, Content-Type  
**Credentials**: Not supported in MVP

## API Versioning

**Current Version**: v1  
**Version Strategy**: URL-based versioning (`/api/v1/...`)  
**Future Versions**: v2, v3 (backward compatible when possible)

## OpenAPI/Swagger Documentation

**Swagger UI**: `/docs` (FastAPI auto-generated)  
**ReDoc**: `/redoc` (Alternative documentation)

**Access**: Protected by authentication in production

---

**Document Owner**: Development Team  
**Last Updated**: Current Date  
**Status**: ✅ Complete
