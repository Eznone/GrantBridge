# Frontend-Backend Integration Guide

## Overview

This document describes the integration between the GrantBridge frontend (Next.js) and backend (Django + Ninja API).

## Architecture

### API Client Layer

**Location**: `frontend/src/lib/services/api-client.ts`

The API client provides a centralized HTTP client with:

- Automatic authentication token handling
- Error handling and response parsing
- Type-safe request methods (GET, POST, PUT, PATCH, DELETE)
- Query parameter serialization

### Service Layer

Service files encapsulate all API calls for specific domains:

1. **Grant Service** (`frontend/src/lib/services/grant-service.ts`)
   - List grants with filters
   - Get grant details
   - Save/unsave grants
   - Get applications

2. **Proposal Service** (`frontend/src/lib/services/proposal-service.ts`)
   - CRUD operations for proposals
   - Submit proposals
   - Version management
   - Export to PDF/DOCX

3. **Dashboard Service** (`frontend/src/lib/services/dashboard-service.ts`)
   - Dashboard statistics
   - Upcoming deadlines
   - Notifications
   - Analytics data

4. **Matching Service** (`frontend/src/lib/services/matching-service.ts`)
   - Get grant matches
   - Calculate matches
   - Match statistics

### Custom Hooks Layer

React hooks provide data fetching with loading and error states:

1. **useGrants** (`frontend/src/lib/hooks/use-grants.ts`)
   - `useGrants(filters)` - List grants with filters
   - `useGrant(id)` - Get single grant
   - `useSavedGrants()` - Get saved grants

2. **useProposals** (`frontend/src/lib/hooks/use-proposals.ts`)
   - `useProposals(filters)` - List proposals
   - `useProposal(id)` - Get single proposal

3. **useDashboard** (`frontend/src/lib/hooks/use-dashboard.ts`)
   - `useDashboardStats()` - Get dashboard statistics
   - `useUpcomingDeadlines(days)` - Get upcoming deadlines

4. **useMatching** (`frontend/src/lib/hooks/use-matching.ts`)
   - `useMatches(filters)` - Get grant matches
   - `useTopMatches(limit)` - Get top matches
   - `useMatchStats()` - Get match statistics

## Updated Pages

### Dashboard Page

**Location**: `frontend/src/app/dashboard/page.tsx`

**Changes**:

- Replaced mock data with real API calls
- Added loading states with `LoadingSpinner`
- Added error handling with `ErrorState`
- Fetches dashboard stats, top matches, and proposals
- Displays real-time data from backend

**API Endpoints Used**:

- `GET /api/v1/dashboard/stats` - Dashboard statistics
- `GET /api/v1/matches/top` - Top grant matches
- `GET /api/v1/proposals` - Proposals list

### Grants Page

**Location**: `frontend/src/app/dashboard/grants/page.tsx`

**Changes**:

- Replaced mock grants with API data
- Implemented real-time filtering and search
- Added loading and error states
- Connected to backend grant endpoints

**API Endpoints Used**:

- `GET /api/v1/grants` - List grants with filters

**Filters Supported**:

- Search query
- Categories
- Sort by (deadline, funding amount)
- Pagination

### Proposals Page

**Location**: `frontend/src/app/dashboard/proposals/page.tsx`

**Changes**:

- Loads proposals from backend
- Added loading and error states
- Auto-loads first proposal for editing

**API Endpoints Used**:

- `GET /api/v1/proposals` - List proposals

## Environment Configuration

### Required Environment Variables

Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

For production:

```env
NEXT_PUBLIC_API_URL=https://your-backend-domain.com/api/v1
```

## Authentication Flow

1. User logs in via `/auth/login` endpoint
2. Backend returns JWT token
3. Token stored in `localStorage` as `auth_token`
4. API client automatically includes token in all requests
5. Token sent as `Authorization: Bearer <token>` header

## Error Handling

All API calls include comprehensive error handling:

```typescript
try {
  const data = await apiClient.get("/endpoint");
  // Handle success
} catch (error: ApiError) {
  // error.message - User-friendly error message
  // error.statusCode - HTTP status code
  // error.details - Validation errors (if any)
}
```

## Loading States

All hooks return a consistent interface:

```typescript
const { data, loading, error } = useHook()

if (loading) return <LoadingSpinner />
if (error) return <ErrorState message={error} />
// Render data
```

## Type Safety

All API responses are typed using TypeScript interfaces:

- `Grant` - Grant data structure
- `Proposal` - Proposal data structure
- `DashboardStats` - Dashboard statistics
- `GrantMatch` - Grant match data

## Testing the Integration

### 1. Start Backend Server

```bash
cd backend
python manage.py runserver
```

### 2. Start Frontend Server

```bash
cd frontend
npm run dev
```

### 3. Test Endpoints

**Dashboard**:

- Navigate to `/dashboard`
- Verify stats load from backend
- Check for loading states
- Verify error handling (stop backend to test)

**Grants**:

- Navigate to `/dashboard/grants`
- Test search functionality
- Test category filters
- Verify pagination

**Proposals**:

- Navigate to `/dashboard/proposals`
- Verify proposals load
- Test editing functionality

## API Endpoint Mapping

| Frontend Hook           | Backend Endpoint   | Method | Description          |
| ----------------------- | ------------------ | ------ | -------------------- |
| `useDashboardStats()`   | `/dashboard/stats` | GET    | Dashboard statistics |
| `useGrants(filters)`    | `/grants`          | GET    | List grants          |
| `useGrant(id)`          | `/grants/{id}`     | GET    | Get grant details    |
| `useProposals(filters)` | `/proposals`       | GET    | List proposals       |
| `useProposal(id)`       | `/proposals/{id}`  | GET    | Get proposal details |
| `useTopMatches(limit)`  | `/matches/top`     | GET    | Top grant matches    |
| `useMatches(filters)`   | `/matches`         | GET    | List matches         |

## Common Issues and Solutions

### Issue: CORS Errors

**Solution**: Ensure backend CORS settings allow frontend origin:

```python
# backend/config/settings/development.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

### Issue: 401 Unauthorized

**Solution**: Check authentication token:

1. Verify token exists in localStorage
2. Check token expiration
3. Re-login if needed

### Issue: Network Errors

**Solution**:

1. Verify backend is running
2. Check `NEXT_PUBLIC_API_URL` environment variable
3. Verify network connectivity

### Issue: Type Errors

**Solution**: Ensure frontend types match backend schemas:

1. Check backend schema definitions
2. Update frontend TypeScript interfaces
3. Rebuild frontend

## Next Steps

1. **Add More Endpoints**: Connect remaining pages (analytics, applications, etc.)
2. **Implement Mutations**: Add create, update, delete operations
3. **Add Optimistic Updates**: Update UI before API response
4. **Add Caching**: Implement React Query or SWR for better caching
5. **Add Websockets**: Real-time updates for notifications
6. **Add Retry Logic**: Automatic retry for failed requests
7. **Add Request Cancellation**: Cancel pending requests on unmount

## Performance Optimization

1. **Pagination**: Implemented for large lists
2. **Lazy Loading**: Load data only when needed
3. **Debouncing**: Search queries debounced to reduce API calls
4. **Memoization**: Use React.memo for expensive components
5. **Code Splitting**: Dynamic imports for large components

## Security Considerations

1. **Token Storage**: Consider using httpOnly cookies instead of localStorage
2. **HTTPS**: Always use HTTPS in production
3. **Input Validation**: Validate all user inputs
4. **XSS Protection**: Sanitize user-generated content
5. **CSRF Protection**: Implement CSRF tokens for mutations

## Monitoring and Logging

Consider adding:

1. Error tracking (Sentry, LogRocket)
2. Performance monitoring (Web Vitals)
3. API call logging
4. User analytics

---

**Last Updated**: May 3, 2026
**Author**: Bob (Senior Engineer)
