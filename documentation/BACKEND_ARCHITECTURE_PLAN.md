# Django Backend Architecture Plan for GrantBridge

## Executive Summary

This document outlines the complete backend architecture for GrantBridge, a decoupled AI-powered grant management platform. The backend will be built with Django + Django Ninja, serving as a pure API layer for the React frontend hosted on Vercel.

---

## 1. Communication & Security Architecture

### 1.1 CORS Configuration

**Strategy:** Whitelist-based CORS for production security with development flexibility.

```python
# config/settings/base.py
CORS_ALLOWED_ORIGINS = [
    "https://grantbridge.vercel.app",  # Production frontend
    "https://grantbridge-preview-*.vercel.app",  # Preview deployments
]

# Development settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
```

**Environment-based Configuration:**
- **Development:** `CORS_ALLOW_ALL_ORIGINS = True` for local testing
- **Staging/Production:** Explicit whitelist of Vercel domains
- **Dynamic Preview URLs:** Use regex pattern matching for Vercel preview deployments

### 1.2 Authentication System

**Approach:** Stateless JWT Authentication (suitable for decoupled architecture)

**Library:** `django-ninja-jwt` (FastAPI-style JWT for Django Ninja)

**Token Strategy:**
- **Access Token:** Short-lived (15 minutes), used for API requests
- **Refresh Token:** Long-lived (7 days), stored securely, used to obtain new access tokens
- **Token Storage (Frontend):** 
  - Access token: Memory/state (not localStorage for security)
  - Refresh token: httpOnly cookie or secure localStorage

**Authentication Flow:**

```mermaid
sequenceDiagram
    participant Frontend
    participant Backend
    participant Database
    
    Frontend->>Backend: POST /api/v1/auth/register
    Backend->>Database: Create User & Organization
    Backend-->>Frontend: {user, accessToken, refreshToken}
    
    Frontend->>Backend: POST /api/v1/auth/login
    Backend->>Database: Verify Credentials
    Backend-->>Frontend: {user, accessToken, refreshToken}
    
    Frontend->>Backend: GET /api/v1/grants (Authorization: Bearer token)
    Backend->>Backend: Validate JWT
    Backend->>Database: Fetch Grants
    Backend-->>Frontend: {grants[]}
    
    Frontend->>Backend: POST /api/v1/auth/refresh
    Backend->>Backend: Validate Refresh Token
    Backend-->>Frontend: {accessToken}
```

**Security Features:**
- Password hashing: Django's built-in PBKDF2 (or Argon2)
- Rate limiting on auth endpoints (django-ratelimit)
- Token blacklisting for logout
- HTTPS-only in production
- Secure cookie flags (httpOnly, secure, sameSite)

### 1.3 API Security Headers

```python
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True  # Production only
SESSION_COOKIE_SECURE = True  # Production only
CSRF_COOKIE_SECURE = True  # Production only
```

---

## 2. API Route Design

### 2.1 API Structure Overview

**Base URL:** `/api/v1/`

**API Versioning Strategy:** URL-based versioning for clear contract management

### 2.2 Complete Endpoint Mapping

#### 2.2.1 Authentication Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/auth/register` | Register new user & organization | `{name, email, password, organizationName?}` | `{user, accessToken, refreshToken}` |
| POST | `/auth/login` | User login | `{email, password}` | `{user, accessToken, refreshToken}` |
| POST | `/auth/refresh` | Refresh access token | `{refreshToken}` | `{accessToken}` |
| POST | `/auth/logout` | Logout & blacklist token | `{refreshToken}` | `{message}` |
| GET | `/auth/me` | Get current user | - | `{user}` |

#### 2.2.2 Organization Endpoints

| Method | Endpoint | Description | Auth Required | Response |
|--------|----------|-------------|---------------|----------|
| GET | `/organizations` | List all organizations (admin) | Yes | `{organizations[]}` |
| GET | `/organizations/{id}` | Get organization details | Yes | `{organization}` |
| PUT | `/organizations/{id}` | Update organization profile | Yes | `{organization}` |
| PATCH | `/organizations/{id}` | Partial update organization | Yes | `{organization}` |
| GET | `/organizations/{id}/stats` | Get organization statistics | Yes | `{stats}` |

**Organization Stats Response:**
```json
{
  "activeApplications": 12,
  "totalFundingSought": 485000,
  "matchRate": 87,
  "proposalsDrafted": 24,
  "approvedGrants": 8,
  "pendingApplications": 4
}
```

#### 2.2.3 Grant Endpoints

| Method | Endpoint | Description | Query Params | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/grants` | List all grants with filters | `search, minAmount, maxAmount, tags[], status, sortBy, sortOrder, page, limit` | `{grants[], total, page, pages}` |
| GET | `/grants/{id}` | Get grant details | - | `{grant}` |
| POST | `/grants` | Create new grant (admin) | Grant object | `{grant}` |
| PUT | `/grants/{id}` | Update grant | Grant object | `{grant}` |
| DELETE | `/grants/{id}` | Delete grant (admin) | - | `{message}` |
| GET | `/grants/search` | Semantic search grants | `q, limit` | `{grants[], scores[]}` |
| POST | `/grants/{id}/save` | Save grant for later | - | `{message}` |
| DELETE | `/grants/{id}/save` | Unsave grant | - | `{message}` |

**Grant List Response:**
```json
{
  "grants": [
    {
      "id": "grant-uuid",
      "title": "Community Development Grant 2024",
      "organization": "National Community Foundation",
      "fundingAmount": 50000,
      "deadline": "2024-03-15T23:59:59Z",
      "requirements": "Must serve underserved communities...",
      "tags": ["community", "development", "education"],
      "source": "grants.gov",
      "matchScore": 94,
      "status": "new",
      "description": "Supporting community-led initiatives...",
      "eligibility": ["501(c)(3) status", "Operating for 2+ years"],
      "createdAt": "2024-01-15T10:00:00Z",
      "updatedAt": "2024-02-01T14:30:00Z"
    }
  ],
  "total": 156,
  "page": 1,
  "pages": 16
}
```

#### 2.2.4 Matching Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/matching` | Get matched grants for user's org | `limit, threshold` | `{matches[]}` |
| GET | `/matching/{orgId}` | Get matches for specific org | `limit, threshold` | `{matches[]}` |
| POST | `/matching/calculate` | Trigger match calculation | `{organizationId, grantIds[]}` | `{matches[]}` |

**Match Response:**
```json
{
  "matches": [
    {
      "grant": {},
      "matchScore": 94,
      "matchReasons": [
        "Mission alignment: 95%",
        "Category match: Community Development",
        "Funding range appropriate"
      ],
      "recommendedActions": [
        "Review eligibility requirements",
        "Prepare project timeline",
        "Draft initial proposal"
      ]
    }
  ]
}
```

#### 2.2.5 Proposal Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/proposals` | List user's proposals | `status, grantId, page, limit` | `{proposals[], total}` |
| GET | `/proposals/{id}` | Get proposal details | - | `{proposal}` |
| POST | `/proposals` | Create new proposal | `{grantId, title, content?}` | `{proposal}` |
| PUT | `/proposals/{id}` | Update proposal | `{title?, content?, status?}` | `{proposal}` |
| PATCH | `/proposals/{id}` | Partial update | Partial proposal | `{proposal}` |
| DELETE | `/proposals/{id}` | Delete proposal | - | `{message}` |
| POST | `/proposals/{id}/submit` | Submit proposal | - | `{proposal, message}` |
| GET | `/proposals/{id}/export` | Export as PDF/DOCX | `format` | File download |

#### 2.2.6 AI Service Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/ai/generate-proposal` | Generate proposal draft | `{grantId, organizationId, tone?}` | `{content, metadata}` |
| POST | `/ai/improve-text` | Improve selected text | `{text, action, tone?}` | `{improvedText, suggestions[]}` |
| POST | `/ai/rewrite` | Rewrite text | `{text, tone, style}` | `{rewrittenText}` |
| POST | `/ai/adjust-tone` | Adjust text tone | `{text, targetTone}` | `{adjustedText}` |
| POST | `/ai/summarize` | Summarize text | `{text, maxLength}` | `{summary}` |
| POST | `/ai/expand` | Expand text | `{text, targetLength}` | `{expandedText}` |

**AI Generation Request:**
```json
{
  "grantId": "grant-uuid",
  "organizationId": "org-uuid",
  "tone": "professional",
  "sections": ["executive_summary", "project_description", "budget_narrative"]
}
```

**AI Generation Response:**
```json
{
  "content": "# Executive Summary\n\nOur organization...",
  "metadata": {
    "model": "watsonx.ai/granite-13b",
    "generatedAt": "2024-02-15T10:30:00Z",
    "tokensUsed": 1250,
    "confidence": 0.92
  },
  "suggestions": [
    "Consider adding specific metrics",
    "Include community impact data"
  ]
}
```

#### 2.2.7 Dashboard Endpoints

| Method | Endpoint | Description | Query Params | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/dashboard/stats` | Get dashboard statistics | `period` | `{stats}` |
| GET | `/dashboard/analytics` | Get analytics data | `startDate, endDate` | `{analytics}` |
| GET | `/dashboard/notifications` | Get user notifications | `unread, limit` | `{notifications[]}` |
| PUT | `/dashboard/notifications/{id}/read` | Mark notification as read | - | `{notification}` |

**Dashboard Stats Response:**
```json
{
  "activeApplications": 12,
  "totalFundingSought": 485000,
  "matchRate": 87,
  "proposalsDrafted": 24,
  "trends": {
    "applications": "+12%",
    "funding": "+8%",
    "matchRate": "+5%",
    "proposals": "+18%"
  },
  "recentActivity": [
    {
      "type": "grant_matched",
      "title": "New grant match",
      "message": "Community Development Grant matches your profile",
      "timestamp": "2024-02-15T09:30:00Z"
    }
  ]
}
```

#### 2.2.8 Analytics Endpoints

| Method | Endpoint | Description | Query Params | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/analytics/trends` | Application trends over time | `startDate, endDate, groupBy` | `{trends[]}` |
| GET | `/analytics/categories` | Grant category distribution | - | `{categories[]}` |
| GET | `/analytics/success-rate` | Success rate by category | - | `{rates[]}` |
| GET | `/analytics/funding` | Funding amount trends | `startDate, endDate` | `{funding[]}` |

### 2.3 API Response Standards

**Success Response Format:**
```json
{
  "data": {},
  "message": "Success message",
  "timestamp": "2024-02-15T10:30:00Z"
}
```

**Error Response Format:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "email": ["This field is required"],
      "password": ["Password must be at least 8 characters"]
    }
  },
  "timestamp": "2024-02-15T10:30:00Z"
}
```

**Pagination Format:**
```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 156,
    "pages": 8,
    "hasNext": true,
    "hasPrev": false
  }
}
```

---

## 3. Data Models Schema

### 3.1 Core Models Overview

The backend requires the following models to replace frontend mock data:

1. **User** - Authentication and user management
2. **Organization** - NGO profiles with mission, goals, categories
3. **Grant** - Grant opportunities with requirements and deadlines
4. **Proposal** - AI-generated and user-edited proposals
5. **GrantMatch** - Matching scores between organizations and grants
6. **Notification** - User notifications for various events
7. **Application** - Grant application tracking

### 3.2 Detailed Model Definitions

#### 3.2.1 User Model

```python
# apps/authentication/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
import uuid

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='users'
    )
    role = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('member', 'Member')],
        default='member'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['organization', 'role']),
        ]
```

#### 3.2.2 Organization Model

```python
# apps/organizations/models.py
from django.db import models
import uuid

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    type = models.CharField(max_length=100, default='501(c)(3) Nonprofit')
    ein = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Address
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=100, default='USA')
    
    # Organization Details (matches frontend types)
    mission = models.TextField(help_text="Organization's mission statement")
    description = models.TextField(blank=True)
    goals = models.JSONField(default=list, help_text="List of organizational goals")
    categories = models.JSONField(default=list, help_text="Nonprofit categories/focus areas")
    historical_projects = models.JSONField(default=list, help_text="Past projects")
    
    # Financial
    year_founded = models.IntegerField(null=True, blank=True)
    annual_budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    funding_needs = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Metadata
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # AI/Matching
    embedding_vector = models.JSONField(null=True, blank=True)
    last_embedding_update = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'organizations'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['created_at']),
        ]
```

#### 3.2.3 Grant Model

```python
# apps/grants/models.py
from django.db import models
import uuid

class Grant(models.Model):
    STATUS_CHOICES = [
        ('opportunity', 'Opportunity'),
        ('reviewing', 'Reviewing'),
        ('drafting', 'Drafting'),
        ('submitted', 'Submitted'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500, db_index=True)
    organization = models.CharField(max_length=255, help_text="Funding organization")
    
    # Financial
    funding_amount = models.DecimalField(max_digits=12, decimal_places=2)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Details
    description = models.TextField()
    requirements = models.TextField(help_text="Grant requirements and criteria")
    eligibility = models.JSONField(default=list, help_text="Eligibility criteria")
    
    # Categorization
    tags = models.JSONField(default=list, help_text="Grant tags/keywords")
    categories = models.JSONField(default=list, help_text="Grant categories")
    
    # Dates
    deadline = models.DateTimeField(db_index=True)
    announcement_date = models.DateTimeField(null=True, blank=True)
    award_date = models.DateTimeField(null=True, blank=True)
    
    # Source
    source = models.CharField(max_length=255, help_text="Source (e.g., grants.gov)")
    source_url = models.URLField(blank=True)
    external_id = models.CharField(max_length=255, blank=True, db_index=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='opportunity')
    is_active = models.BooleanField(default=True, db_index=True)
    
    # AI/Matching
    embedding_vector = models.JSONField(null=True, blank=True)
    last_embedding_update = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'grants'
        indexes = [
            models.Index(fields=['deadline', 'is_active']),
            models.Index(fields=['funding_amount']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-deadline']
```

#### 3.2.4 Proposal Model

```python
# apps/proposals/models.py
from django.db import models
import uuid

class Proposal(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grant = models.ForeignKey('grants.Grant', on_delete=models.CASCADE, related_name='proposals')
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='proposals')
    created_by = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, related_name='created_proposals')
    
    # Content
    title = models.CharField(max_length=500)
    content = models.TextField(help_text="Proposal content in markdown/HTML")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    
    # AI Generation
    ai_generated = models.BooleanField(default=False)
    ai_model_used = models.CharField(max_length=100, blank=True)
    generation_metadata = models.JSONField(null=True, blank=True)
    
    # Submission
    submitted_at = models.DateTimeField(null=True, blank=True)
    submission_method = models.CharField(max_length=100, blank=True)
    
    # Versioning
    version = models.IntegerField(default=1)
    parent_version = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='versions')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'proposals'
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['grant', 'status']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-updated_at']
```

#### 3.2.5 GrantMatch Model

```python
# apps/matching/models.py
from django.db import models
import uuid

class GrantMatch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='grant_matches')
    grant = models.ForeignKey('grants.Grant', on_delete=models.CASCADE, related_name='organization_matches')
    
    # Matching Score
    match_score = models.FloatField(db_index=True, help_text="0-100 compatibility score")
    
    # Match Details
    match_reasons = models.JSONField(default=list, help_text="List of reasons for match")
    recommended_actions = models.JSONField(default=list, help_text="Suggested next steps")
    
    # Match Metadata
    algorithm_version = models.CharField(max_length=50, default='v1.0')
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    # User Interaction
    is_saved = models.BooleanField(default=False)
    is_dismissed = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'grant_matches'
        unique_together = [['organization', 'grant']]
        indexes = [
            models.Index(fields=['organization', 'match_score']),
            models.Index(fields=['grant', 'match_score']),
            models.Index(fields=['-match_score']),
        ]
        ordering = ['-match_score']
```

#### 3.2.6 Notification Model

```python
# apps/core/models.py
from django.db import models
import uuid

class Notification(models.Model):
    TYPE_CHOICES = [
        ('grant_matched', 'Grant Matched'),
        ('application_approved', 'Application Approved'),
        ('application_rejected', 'Application Rejected'),
        ('deadline_reminder', 'Deadline Reminder'),
        ('proposal_generated', 'Proposal Generated'),
        ('system', 'System Notification'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='notifications')
    
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    
    # Links
    link_url = models.CharField(max_length=500, blank=True)
    related_grant = models.ForeignKey('grants.Grant', on_delete=models.SET_NULL, null=True, blank=True)
    related_proposal = models.ForeignKey('proposals.Proposal', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False, db_index=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['-created_at']),
        ]
        ordering = ['-created_at']
```

#### 3.2.7 Application Model (for tracking)

```python
# apps/grants/models.py
class Application(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grant = models.ForeignKey('Grant', on_delete=models.CASCADE, related_name='applications')
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='applications')
    proposal = models.OneToOneField('proposals.Proposal', on_delete=models.SET_NULL, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    progress = models.IntegerField(default=0, help_text="Completion percentage 0-100")
    
    submitted_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'applications'
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['grant', 'status']),
        ]
```

### 3.3 Model Relationships Diagram

```mermaid
erDiagram
    User ||--o{ Proposal : creates
    User }o--|| Organization : belongs_to
    User ||--o{ Notification : receives
    
    Organization ||--o{ Proposal : submits
    Organization ||--o{ GrantMatch : has
    Organization ||--o{ Application : submits
    
    Grant ||--o{ Proposal : receives
    Grant ||--o{ GrantMatch : matched_with
    Grant ||--o{ Application : receives
    
    Proposal }o--|| Grant : for
    Proposal }o--|| Organization : from
    
    Application }o--|| Grant : for
    Application }o--|| Organization : from
    Application }o--o| Proposal : includes
    
    GrantMatch }o--|| Organization : for
    GrantMatch }o--|| Grant : matches
    
    Notification }o--|| User : notifies
    Notification }o--o| Grant : about
    Notification }o--o| Proposal : about
```

---

## 4. AI Service Layer Architecture

### 4.1 AI Service Structure

```
apps/ai/
├── __init__.py
├── services/
│   ├── __init__.py
│   ├── base.py              # Base AI service class
│   ├── matching.py          # Grant matching service
│   ├── generation.py        # Proposal generation service
│   ├── improvement.py       # Text improvement service
│   └── embeddings.py        # Vector embedding service
├── providers/
│   ├── __init__.py
│   ├── base.py              # Base provider interface
│   ├── watsonx.py           # IBM watsonx.ai provider
│   ├── openai.py            # OpenAI provider (optional)
│   └── anthropic.py         # Anthropic provider (optional)
├── prompts/
│   ├── __init__.py
│   ├── matching/
│   │   ├── system.txt
│   │   └── user_template.txt
│   ├── generation/
│   │   ├── executive_summary.txt
│   │   ├── project_description.txt
│   │   └── budget_narrative.txt
│   └── improvement/
│       ├── rewrite.txt
│       ├── expand.txt
│       └── tone_adjust.txt
└── pipelines/
    ├── __init__.py
    ├── matching_pipeline.py
    └── generation_pipeline.py
```

### 4.2 Key AI Services

#### Grant Matching Service
- Semantic similarity between organization mission and grant requirements
- Category-based matching
- Funding range compatibility
- Historical project relevance

#### Proposal Generation Service
- Executive summary generation
- Project description drafting
- Budget narrative creation
- Organizational capacity section

#### Text Improvement Service
- Rewrite for clarity
- Tone adjustment (professional, persuasive, concise)
- Text expansion
- Summarization

### 4.3 Vector Store Integration

**Technology:** ChromaDB or FAISS

**Purpose:**
- Store embeddings for organizations and grants
- Enable semantic search
- Fast similarity matching

---

## 5. Infrastructure & Deployment Strategy

### 5.1 Deployment Architecture

```mermaid
graph TB
    subgraph "Frontend - Vercel"
        A[React App]
    end
    
    subgraph "Backend - Railway/Render"
        B[Django + Nginx]
        C[Celery Workers]
        D[Redis]
    end
    
    subgraph "Database - Neon/Supabase"
        E[PostgreSQL]
    end
    
    subgraph "AI Services"
        F[watsonx.ai]
        G[ChromaDB/FAISS]
    end
    
    subgraph "Storage"
        H[Cloudinary/S3]
    end
    
    A -->|HTTPS/JWT| B
    B --> E
    B --> D
    C --> D
    C --> E
    B --> F
    B --> G
    B --> H
```

### 5.2 Platform Recommendations

#### Option 1: Railway (Recommended for PoC)

**Pros:**
- Simple deployment from GitHub
- Built-in PostgreSQL
- Environment variable management
- Automatic HTTPS
- Free tier available

**Configuration:**
```yaml
# railway.json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt && python manage.py collectstatic --noinput"
  },
  "deploy": {
    "startCommand": "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT",
    "healthcheckPath": "/api/v1/health",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

#### Option 2: Render

**Pros:**
- Free tier with PostgreSQL
- Auto-deploy from Git
- Background workers support
- Good documentation

**Configuration:**
```yaml
# render.yaml
services:
  - type: web
    name: grantbridge-api
    env: python
    buildCommand: "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"
    startCommand: "gunicorn config.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
      - key: DATABASE_URL
        fromDatabase:
          name: grantbridge-db
          property: connectionString
  
  - type: worker
    name: grantbridge-celery
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "celery -A config worker -l info"
  
databases:
  - name: grantbridge-db
    databaseName: grantbridge
    user: grantbridge
```

### 5.3 Database Hosting

#### Recommended: Neon PostgreSQL

**Pros:**
- Serverless PostgreSQL
- Generous free tier
- Automatic backups
- Branch databases for testing

**Connection:**
```python
# config/settings/production.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PGDATABASE'),
        'USER': os.getenv('PGUSER'),
        'PASSWORD': os.getenv('PGPASSWORD'),
        'HOST': os.getenv('PGHOST'),
        'PORT': os.getenv('PGPORT', 5432),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}
```

### 5.4 Environment Variables Configuration

#### Backend Environment Variables

```bash
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=grantbridge-api.railway.app,grantbridge-api.onrender.com
DJANGO_SETTINGS_MODULE=config.settings.production

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname
PGHOST=your-neon-host.neon.tech
PGDATABASE=grantbridge
PGUSER=your-user
PGPASSWORD=your-password
PGPORT=5432

# CORS
CORS_ALLOWED_ORIGINS=https://grantbridge.vercel.app,https://grantbridge-*.vercel.app

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_LIFETIME=15  # minutes
JWT_REFRESH_TOKEN_LIFETIME=10080  # 7 days in minutes

# Redis (for Celery)
REDIS_URL=redis://default:password@host:6379

# AI Services
WATSONX_API_KEY=your-watsonx-api-key
WATSONX_PROJECT_ID=your-project-id
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Vector Store
VECTOR_STORE_PATH=/app/vector_store
CHROMA_PERSIST_DIRECTORY=/app/chroma_db

# File Storage (Optional)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Email (Optional)
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@grantbridge.org

# Monitoring (Optional)
SENTRY_DSN=your-sentry-dsn
```

#### Frontend Environment Variables (Vercel)

```bash
# .env.production
NEXT_PUBLIC_API_URL=https://grantbridge-api.railway.app/api/v1
NEXT_PUBLIC_APP_NAME=GrantBridge
NEXT_PUBLIC_APP_URL=https://grantbridge.vercel.app
```

### 5.5 Deployment Workflow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Git as GitHub
    participant Railway as Railway/Render
    participant Vercel as Vercel
    participant DB as Neon PostgreSQL
    
    Dev->>Git: Push to main branch
    Git->>Railway: Trigger deployment
    Railway->>Railway: Build Docker image
    Railway->>Railway: Run migrations
    Railway->>DB: Apply schema changes
    Railway->>Railway: Collect static files
    Railway->>Railway: Start gunicorn
    Railway-->>Dev: Deployment complete
    
    Git->>Vercel: Trigger frontend build
    Vercel->>Vercel: Build Next.js app
    Vercel->>Vercel: Deploy to CDN
    Vercel-->>Dev: Deployment complete
```

---

## 6. Development Roadmap

### Phase 1: Foundation (Week 1)
- [ ] Setup Django project structure
- [ ] Configure Django Ninja API
- [ ] Implement authentication system (JWT)
- [ ] Create core models (User, Organization)
- [ ] Setup CORS configuration
- [ ] Deploy to Railway/Render

### Phase 2: Core Features (Week 2)
- [ ] Implement Grant model and endpoints
- [ ] Implement Proposal model and endpoints
- [ ] Create dashboard statistics endpoints
- [ ] Setup PostgreSQL database
- [ ] Connect frontend to backend

### Phase 3: AI Integration (Week 3)
- [ ] Integrate watsonx.ai provider
- [ ] Implement grant matching service
- [ ] Setup vector store (ChromaDB)
- [ ] Create proposal generation service
- [ ] Implement text improvement endpoints

### Phase 4: Polish & Testing (Week 4)
- [ ] Add comprehensive error handling
- [ ] Implement rate limiting
- [ ] Setup Celery for background tasks
- [ ] Add API documentation
- [ ] Performance optimization
- [ ] Security audit

---

## 7. Mock Data Replacement Strategy

### 7.1 Frontend Mock Data Identified

Based on analysis, the following mock data needs backend endpoints:

1. **Dashboard Stats** (`mockStats`)
   - Active applications count
   - Total funding sought
   - Match rate percentage
   - Proposals drafted count
   - Trends data

2. **Grants List** (`mockGrants`)
   - Grant details with match scores
   - Filtering and search
   - Pagination

3. **Applications** (`mockApplications`)
   - Application status tracking
   - Progress indicators
   - Submission dates

4. **Notifications** (`mockNotifications`)
   - Real-time notifications
   - Read/unread status
   - Notification types

5. **Analytics Data**
   - Application trends over time
   - Grant category distribution
   - Success rates by category
   - Funding amount trends

6. **Organization Profile** (in profile page)
   - Organization details
   - Contact information
   - Mission and goals

### 7.2 API Endpoints to Replace Mock Data

| Frontend Mock Data | Backend Endpoint | Priority |
|-------------------|------------------|----------|
| `mockStats` | `GET /dashboard/stats` | High |
| `mockGrants` | `GET /grants?page=1&limit=20` | High |
| `mockApplications` | `GET /applications` | High |
| `mockNotifications` | `GET /dashboard/notifications` | Medium |
| `applicationTrendData` | `GET /analytics/trends` | Medium |
| `grantCategoryData` | `GET /analytics/categories` | Medium |
| `successRateData` | `GET /analytics/success-rate` | Medium |
| `fundingAmountData` | `GET /analytics/funding` | Medium |
| Organization profile | `GET /organizations/{id}` | High |
| User data | `GET /auth/me` | High |

---

## 8. Security Checklist

- [x] JWT authentication with short-lived tokens
- [x] HTTPS-only in production
- [x] CORS whitelist configuration
- [x] Rate limiting on sensitive endpoints
- [x] SQL injection protection (Django ORM)
- [x] XSS protection headers
- [x] CSRF protection for state-changing operations
- [x] Password hashing (PBKDF2/Argon2)
- [x] Environment variable management
- [x] API key protection
- [x] Input validation and sanitization
- [x] Token blacklisting for logout

---

## 9. Next Steps

1. **Review this plan** with the team
2. **Set up development environment** with Django + Django Ninja
3. **Create initial models** and migrations
4. **Implement authentication** endpoints first
5. **Deploy to Railway/Render** for testing
6. **Connect frontend** to backend API
7. **Iterate and refine** based on feedback

---

## Appendix: Quick Reference

### Essential Commands

```bash
# Create Django project
django-admin startproject config .

# Create apps
python manage.py startapp authentication
python manage.py startapp organizations
python manage.py startapp grants
python manage.py startapp proposals
python manage.py startapp ai

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

### Key Dependencies

```txt
Django==4.2.7
django-ninja==1.0.1
django-ninja-jwt==5.2.8
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
gunicorn==21.2.0
celery==5.3.4
redis==5.0.1
chromadb==0.4.18
ibm-watson-machine-learning==1.0.335
python-dotenv==1.0.0
```

---

**Document Version:** 1.0  
**Last Updated:** 2024-02-15  
**Author:** Backend Architecture Team