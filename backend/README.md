# GrantBridge Backend API

AI-powered grant management platform for NGOs. Built with Django 4.2 and Django Ninja.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL (or Supabase account)
- IBM watsonx.ai account (for AI features)

### Installation

1. **Clone and navigate to backend**

```bash
cd backend
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**

```bash
python manage.py createsuperuser
```

7. **Run development server**

```bash
python manage.py runserver
```

API will be available at `http://localhost:8000/api/`

## 📚 API Documentation

Interactive API documentation available at:

- **Swagger UI**: `http://localhost:8000/api/docs`
- **Health Check**: `http://localhost:8000/api/health`

## 🏗️ Project Structure

```
backend/
├── apps/
│   ├── authentication/    # User authentication & JWT
│   ├── organizations/     # Organization management
│   ├── grants/           # Grant discovery & applications
│   ├── proposals/        # Proposal creation & management
│   ├── matching/         # AI-powered grant matching
│   ├── ai/              # AI services (watsonx.ai, FAISS)
│   └── core/            # Dashboard, notifications, analytics
├── config/
│   ├── settings/        # Environment-specific settings
│   ├── urls.py         # URL configuration
│   ├── wsgi.py         # WSGI configuration
│   └── api.py          # Main API router
├── migrations/          # Database migrations
├── static/             # Static files
├── media/              # User uploads
├── logs/               # Application logs
└── manage.py           # Django management script
```

## 🔑 Key Features

### Authentication

- JWT-based authentication
- Email/password registration
- Token refresh mechanism
- Profile management

### Grant Management

- Advanced search and filtering
- Save/bookmark grants
- Application tracking
- Deadline monitoring

### Proposal System

- Rich text editor support
- Version control
- AI-assisted generation
- Export to PDF/DOCX

### AI-Powered Matching

- Semantic similarity matching
- Category and tag alignment
- Match quality scoring
- Dismissible recommendations

### Dashboard & Analytics

- Real-time statistics
- Upcoming deadlines
- Recent activity tracking
- Notification system

## 🔧 Configuration

### Environment Variables

See `.env.example` for all available configuration options.

**Required:**

- `DJANGO_SECRET_KEY` - Django secret key
- `DATABASE_URL` - PostgreSQL connection string
- `WATSONX_API_KEY` - IBM watsonx.ai API key
- `WATSONX_PROJECT_ID` - IBM watsonx.ai project ID

**Optional:**

- `CORS_ALLOWED_ORIGINS` - Frontend URLs
- `EMAIL_HOST` - SMTP server
- `SENTRY_DSN` - Error tracking

### Database

**Development (SQLite):**

```python
# Default - no configuration needed
```

**Production (Supabase):**

```bash
DATABASE_URL=postgresql://user:pass@host:port/db?sslmode=require
```

## 🚢 Deployment

### Render.com

1. **Connect repository** to Render
2. **Use Blueprint**: `render.yaml` is pre-configured
3. **Set environment variables** in Render dashboard
4. **Deploy**: Automatic on push to main branch

### Manual Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate --no-input

# Start with Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=apps

# Specific app
pytest apps/authentication/tests/
```

## 📊 API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user
- `PUT /api/auth/profile` - Update profile

### Grants

- `GET /api/grants` - List grants (with filters)
- `GET /api/grants/{id}` - Get grant details
- `POST /api/grants/{id}/save` - Save grant
- `DELETE /api/grants/{id}/save` - Unsave grant
- `GET /api/grants/saved` - List saved grants

### Proposals

- `GET /api/proposals` - List proposals
- `POST /api/proposals` - Create proposal
- `GET /api/proposals/{id}` - Get proposal
- `PUT /api/proposals/{id}` - Update proposal
- `DELETE /api/proposals/{id}` - Delete proposal
- `POST /api/proposals/{id}/submit` - Submit proposal
- `POST /api/proposals/{id}/export` - Export to PDF/DOCX

### Matching

- `GET /api/matches` - Get grant matches
- `POST /api/matches/calculate` - Calculate matches
- `POST /api/matches/{id}/dismiss` - Dismiss match
- `GET /api/matches/stats` - Match statistics

### Dashboard

- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/dashboard/deadlines` - Upcoming deadlines

### Notifications

- `GET /api/notifications` - List notifications
- `POST /api/notifications/{id}/read` - Mark as read
- `POST /api/notifications/read-all` - Mark all as read

## 🔒 Security

- HTTPS enforced in production
- CORS configured for Vercel frontend
- JWT token authentication
- CSRF protection
- SQL injection prevention
- XSS protection headers
- Rate limiting on auth endpoints

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Run tests
4. Submit pull request

## 📝 License

Proprietary - IBM Consulting

## 🆘 Support

For issues and questions:

- Check documentation in `/documentation`
- Review API docs at `/api/docs`
- Contact: support@grantbridge.org

---

**Made with ❤️ by Bob**
