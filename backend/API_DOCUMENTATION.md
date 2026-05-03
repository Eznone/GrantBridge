# GrantBridge API Documentation

Complete API reference with examples for the GrantBridge backend.

## Base URL

```
Development: http://localhost:8000/api
Production: https://your-domain.com/api
```

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

---

## Table of Contents

1. [Authentication](#authentication-endpoints)
2. [Organizations](#organization-endpoints)
3. [Grants](#grant-endpoints)
4. [Proposals](#proposal-endpoints)
5. [Matching](#matching-endpoints)
6. [Dashboard & Analytics](#dashboard--analytics-endpoints)
7. [Notifications](#notification-endpoints)

---

## Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /auth/register`

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe",
  "organization_name": "Example NGO"
}
```

**Response:** `201 Created`

```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Rate Limit:** 3 requests per hour per IP

---

### Login

Authenticate and receive JWT tokens.

**Endpoint:** `POST /auth/login`

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response:** `200 OK`

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**Rate Limit:** 5 requests per 5 minutes per IP

---

### Refresh Token

Get a new access token using refresh token.

**Endpoint:** `POST /auth/refresh`

**Request Body:**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK`

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Rate Limit:** 10 requests per 5 minutes per IP

---

## Organization Endpoints

### Get My Organization

Get the current user's organization details.

**Endpoint:** `GET /organizations/me`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

```json
{
  "id": 1,
  "name": "Example NGO",
  "mission": "Improving education in underserved communities",
  "description": "We provide educational resources...",
  "website": "https://example-ngo.org",
  "annual_budget": 500000.0,
  "goals": ["Increase literacy", "Provide scholarships"],
  "categories": ["education", "youth development"],
  "tags": ["education", "community"],
  "contact_email": "contact@example-ngo.org",
  "contact_phone": "+1234567890",
  "address": "123 Main St",
  "city": "New York",
  "country": "USA",
  "founded_year": 2010
}
```

---

### Update Organization

Update organization details.

**Endpoint:** `PUT /organizations/me`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**

```json
{
  "name": "Example NGO",
  "mission": "Updated mission statement",
  "annual_budget": 600000.0,
  "goals": ["New goal 1", "New goal 2"],
  "categories": ["education", "health"]
}
```

**Response:** `200 OK` (returns updated organization)

---

## Grant Endpoints

### List Grants

Get a paginated list of grants with optional filters.

**Endpoint:** `GET /grants`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**

- `page` (int): Page number (default: 1)
- `page_size` (int): Items per page (default: 20)
- `search` (string): Search in title and description
- `categories` (string): Comma-separated categories
- `tags` (string): Comma-separated tags
- `min_amount` (float): Minimum grant amount
- `max_amount` (float): Maximum grant amount
- `deadline_after` (date): Filter by deadline (YYYY-MM-DD)
- `deadline_before` (date): Filter by deadline (YYYY-MM-DD)

**Example Request:**

```
GET /grants?categories=education,health&min_amount=10000&page=1
```

**Response:** `200 OK`

```json
{
  "count": 150,
  "next": "/grants?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Education Innovation Grant",
      "funder_name": "Example Foundation",
      "description": "Supporting innovative education programs...",
      "amount_min": 10000.0,
      "amount_max": 50000.0,
      "deadline": "2026-12-31T23:59:59Z",
      "categories": ["education", "innovation"],
      "tags": ["K-12", "technology"],
      "eligibility": "501(c)(3) organizations",
      "application_url": "https://foundation.org/apply",
      "created_at": "2026-01-01T00:00:00Z"
    }
  ]
}
```

---

### Get Grant Details

Get detailed information about a specific grant.

**Endpoint:** `GET /grants/{id}`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

```json
{
  "id": 1,
  "title": "Education Innovation Grant",
  "funder_name": "Example Foundation",
  "funder_website": "https://foundation.org",
  "description": "Detailed description...",
  "amount_min": 10000.0,
  "amount_max": 50000.0,
  "currency": "USD",
  "deadline": "2026-12-31T23:59:59Z",
  "categories": ["education", "innovation"],
  "tags": ["K-12", "technology"],
  "eligibility": "501(c)(3) organizations",
  "focus_areas": ["STEM education", "Teacher training"],
  "geographic_scope": ["United States"],
  "application_url": "https://foundation.org/apply",
  "requirements": "Detailed requirements...",
  "created_at": "2026-01-01T00:00:00Z",
  "updated_at": "2026-01-15T00:00:00Z"
}
```

---

### Save Grant

Bookmark a grant for later.

**Endpoint:** `POST /grants/{id}/save`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

```json
{
  "message": "Grant saved successfully"
}
```

---

### Unsave Grant

Remove a grant from bookmarks.

**Endpoint:** `DELETE /grants/{id}/save`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

```json
{
  "message": "Grant removed from saved list"
}
```

---

## Proposal Endpoints

### List Proposals

Get all proposals for the organization.

**Endpoint:** `GET /proposals`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**

- `status` (string): Filter by status (draft, submitted, approved, rejected)
- `grant_id` (int): Filter by grant

**Response:** `200 OK`

```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "title": "Education Program Proposal",
      "grant": {
        "id": 1,
        "title": "Education Innovation Grant"
      },
      "status": "draft",
      "amount_requested": 25000.0,
      "created_at": "2026-01-01T00:00:00Z",
      "updated_at": "2026-01-15T00:00:00Z",
      "submitted_at": null
    }
  ]
}
```

---

### Create Proposal

Create a new proposal.

**Endpoint:** `POST /proposals`

**Headers:** `Authorization: Bearer <token>`

**Request Body:**

```json
{
  "grant_id": 1,
  "title": "My Proposal Title",
  "executive_summary": "Brief summary...",
  "project_description": "Detailed description...",
  "budget_justification": "Budget explanation...",
  "amount_requested": 25000.0
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "title": "My Proposal Title",
  "grant": {
    "id": 1,
    "title": "Education Innovation Grant"
  },
  "status": "draft",
  "amount_requested": 25000.0,
  "created_at": "2026-01-01T00:00:00Z"
}
```

---

### Submit Proposal

Submit a proposal for review.

**Endpoint:** `POST /proposals/{id}/submit`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

```json
{
  "message": "Proposal submitted successfully",
  "proposal": {
    "id": 1,
    "status": "submitted",
    "submitted_at": "2026-01-15T10:30:00Z"
  }
}
```

---

## Matching Endpoints

### Get Matches

Get grant matches for the organization.

**Endpoint:** `GET /matches`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**

- `min_score` (int): Minimum match score (0-100)
- `quality` (string): Filter by quality (excellent, good, fair, poor)
- `dismissed` (bool): Include dismissed matches

**Response:** `200 OK`

```json
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "grant": {
        "id": 1,
        "title": "Education Innovation Grant",
        "amount_max": 50000.0,
        "deadline": "2026-12-31T23:59:59Z"
      },
      "match_score": 85.5,
      "match_quality": "excellent",
      "reasoning": "Strong alignment with organization's mission...",
      "strengths": ["Category match", "Budget alignment", "Geographic fit"],
      "concerns": ["Tight deadline"],
      "recommendations": [
        "Emphasize past success in similar programs",
        "Highlight community partnerships"
      ],
      "is_dismissed": false,
      "created_at": "2026-01-01T00:00:00Z"
    }
  ]
}
```

---

### Calculate Matches

Trigger match calculation for the organization.

**Endpoint:** `POST /matches/calculate`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

```json
{
  "message": "Match calculation completed",
  "matches_created": 15,
  "matches_updated": 5
}
```

---

## Dashboard & Analytics Endpoints

### Dashboard Statistics

Get comprehensive dashboard statistics.

**Endpoint:** `GET /dashboard/stats`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

```json
{
  "total_proposals": 25,
  "active_applications": 10,
  "saved_grants": 15,
  "pending_matches": 20,
  "success_rate": 35.5,
  "total_funding": 250000.0
}
```

---

### Analytics Trends

Get time-series analytics data.

**Endpoint:** `GET /analytics/trends`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**

- `days` (int): Number of days to analyze (default: 90)

**Response:** `200 OK`

```json
{
  "proposals": [
    { "date": "2026-01-01", "count": 5 },
    { "date": "2026-01-02", "count": 3 }
  ],
  "applications": [
    { "date": "2026-01-01", "count": 2 },
    { "date": "2026-01-02", "count": 4 }
  ],
  "matches": [
    { "date": "2026-01-01", "count": 10 },
    { "date": "2026-01-02", "count": 8 }
  ],
  "period_days": 90
}
```

---

### Success Rate Analytics

Get detailed success rate analysis.

**Endpoint:** `GET /analytics/success-rate`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

```json
{
  "overall_success_rate": 35.5,
  "total_applications": 50,
  "successful_applications": 18,
  "by_category": [
    {
      "category": "education",
      "success_rate": 40.0,
      "total_applications": 30
    }
  ],
  "by_amount_range": [
    {
      "range_label": "$10K - $50K",
      "min_amount": 10000.0,
      "max_amount": 50000.0,
      "success_rate": 45.0,
      "total_applications": 20
    }
  ]
}
```

---

## Notification Endpoints

### List Notifications

Get notifications for the user.

**Endpoint:** `GET /notifications`

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**

- `unread_only` (bool): Only return unread notifications

**Response:** `200 OK`

```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "type": "grant_match",
      "title": "New Grant Match",
      "message": "We found a new grant that matches your profile",
      "is_read": false,
      "created_at": "2026-01-15T10:00:00Z",
      "related_object_id": 5
    }
  ]
}
```

---

### Mark Notification as Read

Mark a notification as read.

**Endpoint:** `POST /notifications/{id}/read`

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

```json
{
  "message": "Notification marked as read"
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request

```json
{
  "detail": "Invalid input data",
  "errors": {
    "email": ["This field is required"]
  }
}
```

### 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided"
}
```

### 403 Forbidden

```json
{
  "detail": "You do not have permission to perform this action"
}
```

### 404 Not Found

```json
{
  "detail": "Resource not found"
}
```

### 429 Too Many Requests

```json
{
  "detail": "Rate limit exceeded. Please try again later.",
  "retry_after": 300
}
```

### 500 Internal Server Error

```json
{
  "detail": "An internal server error occurred"
}
```

---

## Rate Limiting

Authentication endpoints have rate limits to prevent abuse:

- **Register:** 3 requests per hour per IP
- **Login:** 5 requests per 5 minutes per IP
- **Refresh:** 10 requests per 5 minutes per IP
- **Change Password:** 3 requests per hour per IP

When rate limited, the API returns a 429 status code with a `retry_after` field indicating seconds until the limit resets.

---

## Pagination

List endpoints support pagination with the following parameters:

- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

Paginated responses include:

```json
{
  "count": 150,
  "next": "/endpoint?page=2",
  "previous": null,
  "results": [...]
}
```

---

## Interactive Documentation

Visit `/api/docs` for interactive Swagger UI documentation where you can test endpoints directly.

---

## Support

For API support, please contact: support@grantbridge.com

**Made with Bob**
