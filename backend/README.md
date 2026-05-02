# GrantBridge Backend

Django + Django Ninja API backend for the GrantBridge AI-powered grant management platform.

## Technology Stack

- **Framework**: Django 4.2.7 + Django Ninja 1.0.1
- **Database**: Supabase (PostgreSQL)
- **Vector Store**: FAISS
- **AI Provider**: IBM watsonx.ai
- **Authentication**: JWT (django-ninja-jwt)
- **Deployment**: Render

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL (or use Supabase)
- pip and virtualenv

### Installation

1. **Create and activate virtual environment**:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

2. **Install dependencies**:

```bash
pip install -r requirements/development.txt
```

3. **Set up environment variables**:

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your configuration
# At minimum, set:
# - DJANGO_SECRET_KEY
# - DATABASE_URL
# - JWT_SECRET_KEY
```

4. **Run migrations**:

```bash
python manage.py migrate
```

5. **Create superuser**:

```bash
python manage.py createsuperuser
```

6. **Run development server**:

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/v1/`

## Project Structure

```
backend/
├── config/                 # Django project configuration
│   ├── settings/          # Settings split by environment
│   │   ├── base.py       # Base settings
│   │   ├── development.py # Development settings
│   │   └── production.py  # Production settings
│   ├── api.py            # Main API router
│   ├── urls.py           # URL configuration
│   ├── wsgi.py           # WSGI configuration
│   └── asgi.py           # ASGI configuration
├── apps/                  # Django applications
│   ├── authentication/   # User authentication & JWT
│   ├── organizations/    # NGO organization management
│   ├── grants/          # Grant opportunities
│   ├── proposals/       # Proposal management
│   ├── matching/        # Grant matching logic
│   ├── ai/             # AI services layer
│   └── core/           # Shared utilities
├── requirements/        # Python dependencies
│   ├── base.txt        # Base requirements
│   ├── development.txt # Development requirements
│   └── production.txt  # Production requirements
├── manage.py           # Django management script
├── .env.example        # Environment variables template
└── README.md          # This file
```

## API Documentation

Once the server is running, visit:

- **Interactive API Docs**: `http://localhost:8000/api/v1/docs`
- **OpenAPI Schema**: `http://localhost:8000/api/v1/openapi.json`

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout user
- `GET /api/v1/auth/me` - Get current user

### Organizations

- `GET /api/v1/organizations/` - List organizations
- `GET /api/v1/organizations/{id}` - Get organization details
- `PUT /api/v1/organizations/{id}` - Update organization
- `GET /api/v1/organizations/{id}/stats` - Get organization statistics

### Grants

- `GET /api/v1/grants/` - List grants (with filtering)
- `GET /api/v1/grants/{id}` - Get grant details
- `POST /api/v1/grants/` - Create grant (admin)
- `PUT /api/v1/grants/{id}` - Update grant (admin)
- `DELETE /api/v1/grants/{id}` - Delete grant (admin)

### Proposals

- `GET /api/v1/proposals/` - List proposals
- `GET /api/v1/proposals/{id}` - Get proposal details
- `POST /api/v1/proposals/` - Create proposal
- `PUT /api/v1/proposals/{id}` - Update proposal
- `DELETE /api/v1/proposals/{id}` - Delete proposal

### Matching

- `GET /api/v1/matching/` - Get matched grants
- `POST /api/v1/matching/calculate` - Calculate matches

### AI Services

- `POST /api/v1/ai/generate-proposal` - Generate proposal draft
- `POST /api/v1/ai/improve-text` - Improve text
- `POST /api/v1/ai/rewrite` - Rewrite text
- `POST /api/v1/ai/adjust-tone` - Adjust tone
- `POST /api/v1/ai/summarize` - Summarize text
- `POST /api/v1/ai/expand` - Expand text

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
```

### Linting

```bash
flake8
```

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations
```

### Django Shell

```bash
python manage.py shell
```

### Create Sample Data

```bash
python manage.py seed_data
```

## Environment Variables

See `.env.example` for all available environment variables.

### Required Variables

- `DJANGO_SECRET_KEY` - Django secret key
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET_KEY` - JWT signing key

### Optional Variables

- `WATSONX_API_KEY` - IBM watsonx.ai API key
- `WATSONX_PROJECT_ID` - IBM watsonx.ai project ID
- `SENTRY_DSN` - Sentry error tracking DSN
- `REDIS_URL` - Redis connection URL (for Celery)

## Deployment

### Render Deployment

1. **Connect GitHub repository** to Render
2. **Set environment variables** in Render dashboard
3. **Deploy** - Render will automatically:
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start gunicorn server

See `render.yaml` for deployment configuration.

### Supabase Database Setup

1. **Create Supabase project**
2. **Get connection string** from project settings
3. **Set DATABASE_URL** environment variable
4. **Run migrations** to create tables

## Troubleshooting

### Database Connection Issues

- Verify DATABASE_URL is correct
- Check PostgreSQL is running
- Ensure database exists

### Import Errors

- Activate virtual environment
- Install requirements: `pip install -r requirements/development.txt`

### Migration Issues

- Delete migration files (except `__init__.py`)
- Run `python manage.py makemigrations`
- Run `python manage.py migrate`

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

Proprietary - IBM Hackathon Project

## Support

For issues and questions, please contact the development team.
