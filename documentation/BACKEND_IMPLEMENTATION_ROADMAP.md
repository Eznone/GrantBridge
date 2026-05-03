# GrantBridge Backend Implementation Roadmap

## Technology Stack (Confirmed)

- **Framework**: Django 4.2.7 + Django Ninja 1.0.1
- **Database**: Supabase (PostgreSQL)
- **Vector Store**: FAISS
- **Deployment**: Render
- **AI Provider**: IBM watsonx.ai
- **Authentication**: JWT (django-ninja-jwt)
- **Background Tasks**: Deferred to Phase 3 (Celery + Redis)

---

## Phase 1: Foundation & Core Setup (Week 1)

### 1.1 Project Initialization

**Goal**: Set up Django project structure with proper configuration

**Tasks**:

- [ ] Create Django project with `django-admin startproject config .`
- [ ] Create Django apps:
  - `authentication` - User management and JWT auth
  - `organizations` - NGO profiles
  - `grants` - Grant opportunities
  - `proposals` - Proposal management
  - `matching` - Grant matching logic
  - `ai` - AI services layer
  - `core` - Shared utilities and middleware
- [ ] Set up project structure:
  ```
  backend/
  ├── manage.py
  ├── requirements/
  │   ├── base.txt
  │   ├── development.txt
  │   └── production.txt
  ├── config/
  │   ├── __init__.py
  │   ├── settings/
  │   │   ├── __init__.py
  │   │   ├── base.py
  │   │   ├── development.py
  │   │   └── production.py
  │   ├── urls.py
  │   ├── wsgi.py
  │   └── asgi.py
  └── apps/
      ├── authentication/
      ├── organizations/
      ├── grants/
      ├── proposals/
      ├── matching/
      ├── ai/
      └── core/
  ```

### 1.2 Dependencies Installation

**Goal**: Install all required Python packages

**Create `requirements/base.txt`**:

```txt
Django==4.2.7
django-ninja==1.0.1
django-ninja-jwt==5.2.8
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
python-dotenv==1.0.0
gunicorn==21.2.0

# AI & ML
ibm-watson-machine-learning==1.0.335
faiss-cpu==1.7.4
sentence-transformers==2.2.2

# Utilities
python-dateutil==2.8.2
Pillow==10.1.0
```

**Create `requirements/development.txt`**:

```txt
-r base.txt
django-debug-toolbar==4.2.0
ipython==8.18.1
pytest==7.4.3
pytest-django==4.7.0
black==23.12.0
flake8==6.1.0
```

**Create `requirements/production.txt`**:

```txt
-r base.txt
sentry-sdk==1.39.1
```

### 1.3 Settings Configuration

**Goal**: Configure Django settings for different environments

**Tasks**:

- [ ] Create `config/settings/base.py` with:
  - Installed apps configuration
  - Middleware setup
  - Database configuration (Supabase)
  - Static files configuration
  - Security settings
  - CORS configuration
  - JWT settings
- [ ] Create `config/settings/development.py` with:
  - DEBUG = True
  - CORS_ALLOW_ALL_ORIGINS = True
  - Development database settings
- [ ] Create `config/settings/production.py` with:
  - DEBUG = False
  - CORS whitelist for Vercel
  - Production security settings
  - Supabase connection settings

**Key Configuration Snippets**:

```python
# config/settings/base.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'ninja',
    'corsheaders',

    # Local apps
    'apps.authentication',
    'apps.organizations',
    'apps.grants',
    'apps.proposals',
    'apps.matching',
    'apps.ai',
    'apps.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'authentication.User'

# JWT Configuration
NINJA_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.getenv('JWT_SECRET_KEY', SECRET_KEY),
}
```

### 1.4 Database Models

**Goal**: Create all core data models

**Tasks**:

- [ ] Implement User model in `apps/authentication/models.py`
- [ ] Implement Organization model in `apps/organizations/models.py`
- [ ] Implement Grant model in `apps/grants/models.py`
- [ ] Implement Proposal model in `apps/proposals/models.py`
- [ ] Implement GrantMatch model in `apps/matching/models.py`
- [ ] Implement Notification model in `apps/core/models.py`
- [ ] Implement Application model in `apps/grants/models.py`
- [ ] Create custom User manager for email-based authentication
- [ ] Add model indexes for performance
- [ ] Add model Meta classes with proper ordering

**Model Relationships**:

```
User ──> Organization (Many-to-One)
User ──> Proposal (One-to-Many, created_by)
User ──> Notification (One-to-Many)

Organization ──> Proposal (One-to-Many)
Organization ──> GrantMatch (One-to-Many)
Organization ──> Application (One-to-Many)

Grant ──> Proposal (One-to-Many)
Grant ──> GrantMatch (One-to-Many)
Grant ──> Application (One-to-Many)

Proposal ──> Grant (Many-to-One)
Proposal ──> Organization (Many-to-One)

Application ──> Grant (Many-to-One)
Application ──> Organization (Many-to-One)
Application ──> Proposal (One-to-One, optional)
```

### 1.5 Database Migrations

**Goal**: Generate and apply initial database schema

**Tasks**:

- [ ] Run `python manage.py makemigrations`
- [ ] Review generated migration files
- [ ] Run `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Test database connection with Supabase

### 1.6 Django Ninja API Setup

**Goal**: Configure Django Ninja for API routing

**Tasks**:

- [ ] Create `config/api.py` with main API router
- [ ] Configure API versioning (`/api/v1/`)
- [ ] Set up automatic OpenAPI documentation
- [ ] Configure API authentication
- [ ] Add error handlers

**Example `config/api.py`**:

```python
from ninja import NinjaAPI
from ninja.security import HttpBearer
from apps.authentication.api import router as auth_router
from apps.organizations.api import router as org_router
from apps.grants.api import router as grants_router
from apps.proposals.api import router as proposals_router
from apps.matching.api import router as matching_router
from apps.ai.api import router as ai_router

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        # JWT validation logic
        pass

api = NinjaAPI(
    version='1.0.0',
    title='GrantBridge API',
    description='AI-powered grant management platform API',
    auth=AuthBearer()
)

api.add_router('/auth/', auth_router, tags=['Authentication'])
api.add_router('/organizations/', org_router, tags=['Organizations'])
api.add_router('/grants/', grants_router, tags=['Grants'])
api.add_router('/proposals/', proposals_router, tags=['Proposals'])
api.add_router('/matching/', matching_router, tags=['Matching'])
api.add_router('/ai/', ai_router, tags=['AI Services'])
```

---

## Phase 2: Authentication & Core Endpoints (Week 1-2)

### 2.1 JWT Authentication Implementation

**Goal**: Implement secure JWT-based authentication

**Tasks**:

- [ ] Create authentication schemas in `apps/authentication/schemas.py`:
  - `RegisterSchema`
  - `LoginSchema`
  - `TokenResponseSchema`
  - `UserSchema`
- [ ] Implement authentication endpoints in `apps/authentication/api.py`:
  - `POST /auth/register` - User registration with organization creation
  - `POST /auth/login` - User login with JWT token generation
  - `POST /auth/refresh` - Refresh access token
  - `POST /auth/logout` - Logout and blacklist token
  - `GET /auth/me` - Get current user profile
- [ ] Implement JWT token generation and validation
- [ ] Add password hashing with Django's built-in system
- [ ] Implement token blacklisting for logout

**Example Schema**:

```python
# apps/authentication/schemas.py
from ninja import Schema
from typing import Optional
from datetime import datetime

class RegisterSchema(Schema):
    name: str
    email: str
    password: str
    organization_name: Optional[str] = None

class LoginSchema(Schema):
    email: str
    password: str

class TokenResponseSchema(Schema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class UserSchema(Schema):
    id: str
    email: str
    name: str
    organization_id: str
    role: str
    created_at: datetime
```

### 2.2 Organization Endpoints

**Goal**: Implement organization management endpoints

**Tasks**:

- [ ] Create organization schemas in `apps/organizations/schemas.py`
- [ ] Implement organization endpoints in `apps/organizations/api.py`:
  - `GET /organizations` - List all organizations (admin only)
  - `GET /organizations/{id}` - Get organization details
  - `PUT /organizations/{id}` - Update organization
  - `PATCH /organizations/{id}` - Partial update
  - `GET /organizations/{id}/stats` - Get organization statistics
- [ ] Add permission checks (user must belong to organization)
- [ ] Implement statistics calculation logic

### 2.3 Grant Endpoints

**Goal**: Implement grant management and search

**Tasks**:

- [ ] Create grant schemas in `apps/grants/schemas.py`
- [ ] Implement grant endpoints in `apps/grants/api.py`:
  - `GET /grants` - List grants with filtering and pagination
  - `GET /grants/{id}` - Get grant details
  - `POST /grants` - Create grant (admin only)
  - `PUT /grants/{id}` - Update grant (admin only)
  - `DELETE /grants/{id}` - Delete grant (admin only)
  - `GET /grants/search` - Semantic search (basic text search for now)
  - `POST /grants/{id}/save` - Save grant for later
  - `DELETE /grants/{id}/save` - Unsave grant
- [ ] Implement filtering logic (amount range, tags, status, deadline)
- [ ] Implement pagination with page/limit parameters
- [ ] Add sorting options (deadline, amount, match score)

**Filtering Example**:

```python
@router.get("/", response=List[GrantSchema])
def list_grants(
    request,
    search: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    tags: Optional[List[str]] = Query(None),
    status: Optional[str] = None,
    sort_by: str = "deadline",
    sort_order: str = "asc",
    page: int = 1,
    limit: int = 20
):
    queryset = Grant.objects.filter(is_active=True)

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    if min_amount:
        queryset = queryset.filter(funding_amount__gte=min_amount)

    if max_amount:
        queryset = queryset.filter(funding_amount__lte=max_amount)

    # ... more filtering logic

    return paginate(queryset, page, limit)
```

---

## Phase 3: Proposals & Matching (Week 2)

### 3.1 Proposal Endpoints

**Goal**: Implement proposal management

**Tasks**:

- [ ] Create proposal schemas in `apps/proposals/schemas.py`
- [ ] Implement proposal endpoints in `apps/proposals/api.py`:
  - `GET /proposals` - List user's proposals
  - `GET /proposals/{id}` - Get proposal details
  - `POST /proposals` - Create new proposal
  - `PUT /proposals/{id}` - Update proposal
  - `PATCH /proposals/{id}` - Partial update
  - `DELETE /proposals/{id}` - Delete proposal
  - `POST /proposals/{id}/submit` - Submit proposal
  - `GET /proposals/{id}/export` - Export as PDF/DOCX
- [ ] Implement proposal versioning logic
- [ ] Add export functionality (PDF/DOCX generation)
- [ ] Implement status workflow (draft → review → submitted)

### 3.2 Matching Endpoints

**Goal**: Implement grant matching system

**Tasks**:

- [ ] Create matching schemas in `apps/matching/schemas.py`
- [ ] Implement matching endpoints in `apps/matching/api.py`:
  - `GET /matching` - Get matched grants for user's organization
  - `GET /matching/{org_id}` - Get matches for specific organization
  - `POST /matching/calculate` - Trigger match calculation
- [ ] Implement basic matching algorithm:
  - Category matching
  - Funding range compatibility
  - Keyword matching
  - Mission alignment (text similarity)
- [ ] Calculate match scores (0-100)
- [ ] Generate match reasons and recommended actions

**Basic Matching Algorithm**:

```python
def calculate_match_score(organization, grant):
    score = 0
    reasons = []

    # Category matching (30 points)
    org_categories = set(organization.categories)
    grant_categories = set(grant.categories)
    category_overlap = len(org_categories & grant_categories)
    if category_overlap > 0:
        category_score = min(30, category_overlap * 10)
        score += category_score
        reasons.append(f"Category match: {category_overlap} shared categories")

    # Funding range (20 points)
    if grant.min_amount <= organization.funding_needs <= grant.max_amount:
        score += 20
        reasons.append("Funding range appropriate")

    # Keyword matching (30 points)
    # ... text similarity logic

    # Mission alignment (20 points)
    # ... semantic similarity using embeddings

    return score, reasons
```

### 3.3 Dashboard & Analytics Endpoints

**Goal**: Implement dashboard statistics and analytics

**Tasks**:

- [ ] Create dashboard schemas in `apps/core/schemas.py`
- [ ] Implement dashboard endpoints in `apps/core/api.py`:
  - `GET /dashboard/stats` - Get dashboard statistics
  - `GET /dashboard/analytics` - Get analytics data
  - `GET /dashboard/notifications` - Get user notifications
  - `PUT /dashboard/notifications/{id}/read` - Mark notification as read
- [ ] Implement analytics endpoints in `apps/core/api.py`:
  - `GET /analytics/trends` - Application trends over time
  - `GET /analytics/categories` - Grant category distribution
  - `GET /analytics/success-rate` - Success rate by category
  - `GET /analytics/funding` - Funding amount trends
- [ ] Calculate statistics from database
- [ ] Implement trend calculations

---

## Phase 4: AI Services Integration (Week 3)

### 4.1 AI Service Layer Structure

**Goal**: Set up AI services architecture

**Tasks**:

- [ ] Create AI service structure:
  ```
  apps/ai/
  ├── __init__.py
  ├── services/
  │   ├── __init__.py
  │   ├── base.py
  │   ├── matching.py
  │   ├── generation.py
  │   ├── improvement.py
  │   └── embeddings.py
  ├── providers/
  │   ├── __init__.py
  │   ├── base.py
  │   └── watsonx.py
  ├── prompts/
  │   ├── __init__.py
  │   ├── matching/
  │   ├── generation/
  │   └── improvement/
  └── api.py
  ```
- [ ] Create base service class
- [ ] Create base provider interface

### 4.2 watsonx.ai Provider Implementation

**Goal**: Integrate IBM watsonx.ai

**Tasks**:

- [ ] Create `apps/ai/providers/watsonx.py`
- [ ] Implement watsonx.ai client initialization
- [ ] Implement text generation method
- [ ] Implement embedding generation method
- [ ] Add error handling and retry logic
- [ ] Create setup instructions document

**watsonx.ai Provider Example**:

```python
# apps/ai/providers/watsonx.py
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
import os

class WatsonXProvider:
    def __init__(self):
        self.api_key = os.getenv('WATSONX_API_KEY')
        self.project_id = os.getenv('WATSONX_PROJECT_ID')
        self.url = os.getenv('WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')

        self.credentials = {
            "url": self.url,
            "apikey": self.api_key
        }

    def generate_text(self, prompt, model_id="ibm/granite-13b-chat-v2", max_tokens=1000):
        parameters = {
            GenParams.MAX_NEW_TOKENS: max_tokens,
            GenParams.TEMPERATURE: 0.7,
            GenParams.TOP_P: 0.9,
        }

        model = Model(
            model_id=model_id,
            params=parameters,
            credentials=self.credentials,
            project_id=self.project_id
        )

        response = model.generate_text(prompt=prompt)
        return response

    def generate_embeddings(self, text, model_id="ibm/slate-125m-english-rtrvr"):
        # Embedding generation logic
        pass
```

### 4.3 FAISS Vector Store Integration

**Goal**: Set up FAISS for semantic search

**Tasks**:

- [ ] Create `apps/ai/services/embeddings.py`
- [ ] Implement FAISS index creation
- [ ] Implement embedding storage for organizations
- [ ] Implement embedding storage for grants
- [ ] Create similarity search function
- [ ] Add index persistence to disk

**FAISS Integration Example**:

```python
# apps/ai/services/embeddings.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)

    def generate_embedding(self, text):
        embedding = self.model.encode([text])[0]
        return embedding.tolist()

    def add_to_index(self, embeddings, ids):
        embeddings_array = np.array(embeddings).astype('float32')
        self.index.add(embeddings_array)

    def search(self, query_embedding, k=10):
        query_array = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_array, k)
        return indices[0], distances[0]

    def save_index(self, path):
        faiss.write_index(self.index, path)

    def load_index(self, path):
        self.index = faiss.read_index(path)
```

### 4.4 AI Service Endpoints

**Goal**: Implement AI-powered endpoints

**Tasks**:

- [ ] Create AI schemas in `apps/ai/schemas.py`
- [ ] Implement AI endpoints in `apps/ai/api.py`:
  - `POST /ai/generate-proposal` - Generate proposal draft
  - `POST /ai/improve-text` - Improve selected text
  - `POST /ai/rewrite` - Rewrite text
  - `POST /ai/adjust-tone` - Adjust text tone
  - `POST /ai/summarize` - Summarize text
  - `POST /ai/expand` - Expand text
- [ ] Create prompt templates for each service
- [ ] Implement proposal generation service
- [ ] Implement text improvement services
- [ ] Add AI response caching (optional)

### 4.5 Enhanced Grant Matching with AI

**Goal**: Improve matching with semantic similarity

**Tasks**:

- [ ] Generate embeddings for all organizations
- [ ] Generate embeddings for all grants
- [ ] Update matching algorithm to use embeddings
- [ ] Implement semantic similarity scoring
- [ ] Combine rule-based and AI-based matching

---

## Phase 5: Security & Deployment (Week 3-4)

### 5.1 CORS Configuration

**Goal**: Configure CORS for frontend communication

**Tasks**:

- [ ] Configure CORS in `config/settings/production.py`
- [ ] Whitelist Vercel domains
- [ ] Support Vercel preview deployments with regex
- [ ] Configure CORS headers
- [ ] Test CORS with frontend

**CORS Configuration**:

```python
# config/settings/production.py
CORS_ALLOWED_ORIGINS = [
    "https://grantbridge.vercel.app",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://grantbridge-.*\.vercel\.app$",
]

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

### 5.2 Rate Limiting

**Goal**: Implement rate limiting on sensitive endpoints

**Tasks**:

- [ ] Install `django-ratelimit`
- [ ] Add rate limiting to authentication endpoints
- [ ] Add rate limiting to AI endpoints
- [ ] Configure rate limits per endpoint
- [ ] Add rate limit headers to responses

### 5.3 Security Headers

**Goal**: Add security headers for production

**Tasks**:

- [ ] Configure security headers in `config/settings/production.py`:
  - `SECURE_BROWSER_XSS_FILTER`
  - `SECURE_CONTENT_TYPE_NOSNIFF`
  - `X_FRAME_OPTIONS`
  - `SECURE_SSL_REDIRECT`
  - `SESSION_COOKIE_SECURE`
  - `CSRF_COOKIE_SECURE`
- [ ] Configure HTTPS-only cookies
- [ ] Add security middleware

### 5.4 Render Deployment Configuration

**Goal**: Configure deployment to Render

**Tasks**:

- [ ] Create `render.yaml` configuration file
- [ ] Configure web service settings
- [ ] Configure environment variables
- [ ] Set up health check endpoint
- [ ] Configure build and start commands
- [ ] Set up automatic deployments from GitHub

**render.yaml Example**:

```yaml
services:
  - type: web
    name: grantbridge-api
    env: python
    region: oregon
    plan: free
    buildCommand: "pip install -r requirements/production.txt && python manage.py collectstatic --noinput && python manage.py migrate"
    startCommand: "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
      - key: DJANGO_SETTINGS_MODULE
        value: config.settings.production
      - key: DJANGO_SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: grantbridge-db
          property: connectionString
      - key: WATSONX_API_KEY
        sync: false
      - key: WATSONX_PROJECT_ID
        sync: false
    healthCheckPath: /api/v1/health

databases:
  - name: grantbridge-db
    databaseName: grantbridge
    user: grantbridge
    plan: free
```

### 5.5 Supabase Database Setup

**Goal**: Configure Supabase PostgreSQL connection

**Tasks**:

- [ ] Create Supabase project
- [ ] Get database connection string
- [ ] Configure database settings in production
- [ ] Test database connection
- [ ] Set up database backups
- [ ] Configure connection pooling

**Supabase Connection**:

```python
# config/settings/production.py
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True
    )
}
```

### 5.6 Environment Variables

**Goal**: Set up environment variables management

**Tasks**:

- [ ] Create `.env.example` file
- [ ] Document all required environment variables
- [ ] Set up environment variables in Render
- [ ] Create environment variables documentation
- [ ] Add validation for required variables

**Environment Variables Template**:

```bash
# .env.example

# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=grantbridge-api.onrender.com
DJANGO_SETTINGS_MODULE=config.settings.production

# Database (Supabase)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# CORS
CORS_ALLOWED_ORIGINS=https://grantbridge.vercel.app

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_LIFETIME=15
JWT_REFRESH_TOKEN_LIFETIME=10080

# AI Services (watsonx.ai)
WATSONX_API_KEY=your-watsonx-api-key
WATSONX_PROJECT_ID=your-project-id
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Vector Store
VECTOR_STORE_PATH=/app/vector_store
FAISS_INDEX_PATH=/app/faiss_index

# Optional: Monitoring
SENTRY_DSN=your-sentry-dsn
```

---

## Phase 6: Documentation & Testing (Week 4)

### 6.1 API Documentation

**Goal**: Create comprehensive API documentation

**Tasks**:

- [ ] Document all API endpoints with examples
- [ ] Add request/response schemas
- [ ] Include authentication examples
- [ ] Add error response examples
- [ ] Create Postman collection
- [ ] Leverage Django Ninja's automatic OpenAPI docs

### 6.2 Setup Guides

**Goal**: Create setup and deployment guides

**Tasks**:

- [ ] Write watsonx.ai setup guide
- [ ] Write Supabase setup guide
- [ ] Write Render deployment guide
- [ ] Create local development setup guide
- [ ] Document environment variables
- [ ] Create troubleshooting guide

### 6.3 Database Seed Script

**Goal**: Create sample data for testing

**Tasks**:

- [ ] Create management command for seeding
- [ ] Generate sample organizations
- [ ] Generate sample grants
- [ ] Generate sample proposals
- [ ] Generate sample matches
- [ ] Generate sample notifications
- [ ] Document seed data usage

**Seed Command Example**:

```python
# apps/core/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from apps.organizations.models import Organization
from apps.grants.models import Grant
# ... other imports

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create sample organizations
        org1 = Organization.objects.create(
            name="Community Health Initiative",
            mission="Improving healthcare access in underserved communities",
            # ... other fields
        )

        # Create sample grants
        grant1 = Grant.objects.create(
            title="Community Development Grant 2026",
            organization="National Community Foundation",
            funding_amount=50000,
            # ... other fields
        )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
```

### 6.4 README Documentation

**Goal**: Create comprehensive README

**Tasks**:

- [ ] Write project overview
- [ ] Add features list
- [ ] Include tech stack
- [ ] Add installation instructions
- [ ] Document API endpoints
- [ ] Add deployment instructions
- [ ] Include contributing guidelines

### 6.5 Security Audit

**Goal**: Review and verify security measures

**Tasks**:

- [ ] Review authentication implementation
- [ ] Verify JWT token security
- [ ] Check CORS configuration
- [ ] Verify HTTPS enforcement
- [ ] Review rate limiting
- [ ] Check input validation
- [ ] Verify password hashing
- [ ] Review API permissions
- [ ] Test for common vulnerabilities

---

## Implementation Priority Matrix

### High Priority (Must Have for MVP)

1. ✅ Project setup and configuration
2. ✅ Database models and migrations
3. ✅ Authentication system (JWT)
4. ✅ Organization endpoints
5. ✅ Grant endpoints (list, detail, filtering)
6. ✅ Proposal endpoints (CRUD)
7. ✅ Basic matching algorithm
8. ✅ Dashboard stats endpoint
9. ✅ CORS configuration
10. ✅ Deployment to Render

### Medium Priority (Important for Full Experience)

1. ⚠️ AI proposal generation
2. ⚠️ AI text improvement
3. ⚠️ Semantic search with FAISS
4. ⚠️ Enhanced matching with embeddings
5. ⚠️ Analytics endpoints
6. ⚠️ Notification system
7. ⚠️ Rate limiting
8. ⚠️ Export functionality (PDF/DOCX)

### Low Priority (Nice to Have)

1. 🔵 Celery background tasks
2. 🔵 Advanced analytics
3. 🔵 Email notifications
4. 🔵 File upload support
5. 🔵 Audit logging
6. 🔵 Advanced caching

---

## Success Criteria

### Phase 1 Complete When:

- [ ] Django project runs locally
- [ ] All models created and migrated
- [ ] Database connected to Supabase
- [ ] Admin panel accessible
- [ ] API documentation auto-generated

### Phase 2 Complete When:

- [ ] Users can register and login
- [ ] JWT tokens generated and validated
- [ ] Organizations can be created and updated
- [ ] Grants can be listed and filtered
- [ ] Frontend can authenticate with backend

### Phase 3 Complete When:

- [ ] Proposals can be created and edited
- [ ] Grant matching returns scored results
- [ ] Dashboard shows real statistics
- [ ] Analytics endpoints return data
- [ ] All CRUD operations work

### Phase 4 Complete When:

- [ ] watsonx.ai integration working
- [ ] Proposal generation produces content
- [ ] Text improvement services functional
- [ ] FAISS semantic search operational
- [ ] Enhanced matching uses embeddings

### Phase 5 Complete When:

- [ ] Backend deployed to Render
- [ ] Frontend can connect to production API
- [ ] CORS configured correctly
- [ ] Security headers in place
- [ ] Rate limiting active

### Phase 6 Complete When:

- [ ] API documentation complete
- [ ] Setup guides written
- [ ] Seed data script working
- [ ] README comprehensive
- [ ] Security audit passed

---

## Risk Mitigation

### Technical Risks

1. **watsonx.ai API Limits**: Implement caching and rate limiting
2. **FAISS Performance**: Start with small dataset, optimize later
3. **Database Connection**: Use connection pooling, handle timeouts
4. **Deployment Issues**: Test early and often on Render

### Timeline Risks

1. **AI Integration Complexity**: Start with simple implementations
2. **Scope Creep**: Stick to MVP features first
3. **Learning Curve**: Allocate time for documentation reading

---

## Next Steps

1. **Review this roadmap** and confirm approach
2. **Set up development environment** locally
3. **Create GitHub repository** for version control
4. **Start Phase 1** with project initialization
5. **Deploy early** to catch integration issues
6. **Iterate rapidly** based on frontend needs

---

**Document Version**: 1.0  
**Created**: 2026-05-02  
**Technology Stack**: Django + Django Ninja + Supabase + FAISS + Render + watsonx.ai
