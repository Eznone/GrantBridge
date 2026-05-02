# GrantBridge Backend - Quick Start Implementation Guide

## Technology Stack Summary

- **Framework**: Django 4.2.7 + Django Ninja 1.0.1
- **Database**: Supabase (PostgreSQL)
- **Vector Store**: FAISS
- **Deployment**: Render
- **AI Provider**: IBM watsonx.ai
- **Authentication**: JWT (django-ninja-jwt)

---

## Phase 1: Initial Setup (Day 1)

### Step 1: Create Backend Directory Structure

```bash
# Create backend directory
mkdir backend
cd backend

# Create Django project
django-admin startproject config .

# Create Django apps
python manage.py startapp authentication
python manage.py startapp organizations
python manage.py startapp grants
python manage.py startapp proposals
python manage.py startapp matching
python manage.py startapp ai
python manage.py startapp core
```

### Step 2: Create Requirements Files

Create `requirements/base.txt`:

```txt
Django==4.2.7
django-ninja==1.0.1
django-ninja-jwt==5.2.8
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
python-dotenv==1.0.0
gunicorn==21.2.0
dj-database-url==2.1.0
ibm-watson-machine-learning==1.0.335
faiss-cpu==1.7.4
sentence-transformers==2.2.2
python-dateutil==2.8.2
Pillow==10.1.0
```

Create `requirements/development.txt`:

```txt
-r base.txt
django-debug-toolbar==4.2.0
ipython==8.18.1
pytest==7.4.3
pytest-django==4.7.0
black==23.12.0
flake8==6.1.0
```

Create `requirements/production.txt`:

```txt
-r base.txt
sentry-sdk==1.39.1
```

### Step 3: Install Dependencies

```bash
pip install -r requirements/development.txt
```

### Step 4: Configure Settings Structure

Create `config/settings/` directory:

```bash
mkdir -p config/settings
touch config/settings/__init__.py
touch config/settings/base.py
touch config/settings/development.py
touch config/settings/production.py
```

Move existing `config/settings.py` content to `config/settings/base.py` and update.

### Step 5: Create .env File

Create `.env` in backend root:

```bash
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_SETTINGS_MODULE=config.settings.development

# Database (local development)
DATABASE_URL=postgresql://user:password@localhost:5432/grantbridge

# JWT
JWT_SECRET_KEY=your-jwt-secret

# AI Services (add when ready)
WATSONX_API_KEY=
WATSONX_PROJECT_ID=
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

---

## Phase 2: Database Models (Day 1-2)

### User Model (`apps/authentication/models.py`)

```python
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
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

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['organization', 'role']),
        ]

    def __str__(self):
        return self.email
```

### Organization Model (`apps/organizations/models.py`)

```python
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

    # Organization Details
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

    def __str__(self):
        return self.name
```

### Grant Model (`apps/grants/models.py`)

```python
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

    def __str__(self):
        return self.title
```

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## Phase 3: Django Ninja API Setup (Day 2)

### Create Main API Router (`config/api.py`)

```python
from ninja import NinjaAPI
from ninja.security import HttpBearer
from ninja_jwt.authentication import JWTAuth

api = NinjaAPI(
    version='1.0.0',
    title='GrantBridge API',
    description='AI-powered grant management platform API',
)

# Import routers (will be created)
from apps.authentication.api import router as auth_router
from apps.organizations.api import router as org_router
from apps.grants.api import router as grants_router

# Add routers
api.add_router('/auth/', auth_router, tags=['Authentication'], auth=None)
api.add_router('/organizations/', org_router, tags=['Organizations'], auth=JWTAuth())
api.add_router('/grants/', grants_router, tags=['Grants'], auth=JWTAuth())
```

### Update URLs (`config/urls.py`)

```python
from django.contrib import admin
from django.urls import path
from .api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls),
]
```

---

## Phase 4: Authentication Implementation (Day 2-3)

### Authentication Schemas (`apps/authentication/schemas.py`)

```python
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
    access: str
    refresh: str

class UserSchema(Schema):
    id: str
    email: str
    name: str
    organization_id: Optional[str]
    role: str
    created_at: datetime
```

### Authentication API (`apps/authentication/api.py`)

```python
from ninja import Router
from django.contrib.auth import authenticate
from ninja_jwt.tokens import RefreshToken
from .schemas import RegisterSchema, LoginSchema, TokenResponseSchema, UserSchema
from .models import User
from apps.organizations.models import Organization

router = Router()

@router.post("/register", response=TokenResponseSchema)
def register(request, data: RegisterSchema):
    # Create organization if provided
    organization = None
    if data.organization_name:
        organization = Organization.objects.create(
            name=data.organization_name,
            email=data.email,
            mission="",
        )

    # Create user
    user = User.objects.create_user(
        email=data.email,
        name=data.name,
        password=data.password,
        organization=organization,
        role='admin' if organization else 'member'
    )

    # Generate tokens
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

@router.post("/login", response=TokenResponseSchema)
def login(request, data: LoginSchema):
    user = authenticate(email=data.email, password=data.password)

    if user is None:
        return 401, {"detail": "Invalid credentials"}

    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

@router.get("/me", response=UserSchema)
def get_current_user(request):
    return request.auth
```

---

## Phase 5: Core Endpoints (Day 3-4)

### Grant Endpoints (`apps/grants/api.py`)

```python
from ninja import Router, Query
from typing import List, Optional
from .models import Grant
from .schemas import GrantSchema, GrantListResponseSchema
from django.db.models import Q

router = Router()

@router.get("/", response=GrantListResponseSchema)
def list_grants(
    request,
    search: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    tags: Optional[List[str]] = Query(None),
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

    if tags:
        queryset = queryset.filter(tags__overlap=tags)

    total = queryset.count()
    start = (page - 1) * limit
    end = start + limit

    grants = list(queryset[start:end])

    return {
        'grants': grants,
        'total': total,
        'page': page,
        'pages': (total + limit - 1) // limit
    }

@router.get("/{grant_id}", response=GrantSchema)
def get_grant(request, grant_id: str):
    return Grant.objects.get(id=grant_id)
```

---

## Phase 6: Deployment Configuration (Day 4-5)

### Create `render.yaml`

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
    healthCheckPath: /api/v1/health

databases:
  - name: grantbridge-db
    databaseName: grantbridge
    user: grantbridge
    plan: free
```

### Production Settings (`config/settings/production.py`)

```python
from .base import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True
    )
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "https://grantbridge.vercel.app",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://grantbridge-.*\.vercel\.app$",
]

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

---

## Quick Commands Reference

```bash
# Development
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py shell

# Testing
python manage.py test
pytest

# Code Quality
black .
flake8

# Production
gunicorn config.wsgi:application
python manage.py collectstatic --noinput
```

---

## API Testing with cURL

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"password123","organization_name":"My NGO"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'

# Get Grants (with token)
curl -X GET http://localhost:8000/api/v1/grants/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Next Steps After Setup

1. ✅ Complete remaining models (Proposal, GrantMatch, Notification, Application)
2. ✅ Implement all CRUD endpoints
3. ✅ Add AI services integration
4. ✅ Set up FAISS vector store
5. ✅ Deploy to Render
6. ✅ Connect frontend to backend
7. ✅ Test end-to-end functionality

---

**Ready to implement? Switch to Code mode to begin!**
