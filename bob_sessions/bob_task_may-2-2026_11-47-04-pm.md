**User:**

<task>
Role & Context:
Act as a Senior Software Architect. I am building a decoupled proof-of-concept application. The frontend is built with React and will be hosted on Vercel. I need you to design the backend API, which will be built using Django and PostgreSQL. Aside from the instructions given look intensively into the 'documentation/BACKEND_ARCHITECTURE_PLAN.md' (see below for file content) 

Core Objective:
Plan a backend architecture that strictly acts as an API to serve the React frontend. It needs to be lightweight enough for a PoC but structured correctly for decoupled communication.

Please provide the following deliverables:

Communication & Security: Explain how the React frontend will securely communicate with the Django backend. Specifically address how we will handle CORS configuration and stateless authentication (e.g., JWT or session management suitable for decoupled apps).

API Route Design: Map out the RESTful endpoint structure for our core features, including standard user operations (registration, login, data fetching).

Data Models: Draft the initial Django models.py schema, detailing the relationships between entities.

Infrastructure & Deployment: Provide a brief deployment strategy for hosting this Django backend on a platform suited for traditional servers (like Render or Railway), detailing how the Vercel frontend will connect to it via environment variables.
</task>

<file_content path="documentation/BACKEND_ARCHITECTURE_PLAN.md">
<file_outline>File: BACKEND_ARCHITECTURE_PLAN.md (1191 lines)

No symbols found in this file.</file_outline>
<notice>This file is large (1191 lines). You will use the following strategy to understand this file:
- Inform the user you are going to use large file strategy, to efficiently understand the file
- Use the file_outline provided to get an overview of the file structure to help decide next action. This is not the full file. It is not the full depth of the contents.
- If you read the file, use precise file reads with line ranges for specific sections of interest
- Consider if other commands/tools are better suited for extracting information from that file type
- Use ask_followup_question tool if needed to identify the best next action
</notice>
</file_content>
<environment_details>
# VSCode Visible Files
documentation\BACKEND_ARCHITECTURE_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/BACKEND_ARCHITECTURE_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:45:56.566Z
User time zone: Europe/Madrid, UTC+2:00

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>


# Current Workspace Directory (//wsl.localhost/Ubuntu/home/mrmed/projects/IBM_day/GrantBridge) Files
package-lock.json
bob_sessions/
bob_sessions/.gitkeep
documentation/
documentation/BACKEND_ARCHITECTURE_PLAN.md
documentation/BACKEND_EXECUTION_PLAN.md
documentation/FRONTEND_EXECUTION_PLAN.md
documentation/FRONTEND_IMPLEMENTATION_ROADMAP.md
documentation/QUICK_START_GUIDE.md
documentation/specifications/
documentation/specifications/Ai Grant Assistant Backend Architecture Spec.pdf
documentation/specifications/Ai Grant Assistant Design System Spec.pdf
frontend/
frontend/.gitignore
frontend/components.json
frontend/next.config.js
frontend/package-lock.json
frontend/package.json
frontend/PHASE_4_5_IMPLEMENTATION.md
frontend/postcss.config.js
frontend/README.md
frontend/tailwind.config.ts
frontend/tsconfig.json
frontend/.next/
frontend/src/
frontend/src/app/
frontend/src/app/globals.css
frontend/src/app/layout.tsx
frontend/src/app/page.tsx
frontend/src/app/(auth)/
frontend/src/app/(auth)/layout.tsx
frontend/src/app/(auth)/login/
frontend/src/app/(auth)/login/page.tsx
frontend/src/app/(auth)/register/
frontend/src/app/(auth)/register/page.tsx
frontend/src/app/dashboard/
frontend/src/app/dashboard/layout.tsx
frontend/src/app/dashboard/page.tsx
frontend/src/app/dashboard/ai-assistant/
frontend/src/app/dashboard/ai-assistant/page.tsx
frontend/src/app/dashboard/analytics/
frontend/src/app/dashboard/analytics/page.tsx
frontend/src/app/dashboard/applications/
frontend/src/app/dashboard/applications/page.tsx
frontend/src/app/dashboard/grants/
frontend/src/app/dashboard/grants/page.tsx
frontend/src/app/dashboard/profile/
frontend/src/app/dashboard/profile/page.tsx
frontend/src/app/dashboard/proposals/
frontend/src/app/dashboard/proposals/page.tsx
frontend/src/app/dashboard/settings/
frontend/src/app/dashboard/settings/page.tsx
frontend/src/components/
frontend/src/components/dashboard/
frontend/src/components/dashboard/analytics-overview.tsx
frontend/src/components/dashboard/stat-cards.tsx
frontend/src/components/layout/
frontend/src/components/layout/sidebar.tsx
frontend/src/components/layout/topbar.tsx
frontend/src/components/proposals/
frontend/src/components/proposals/ai-suggestions.tsx
frontend/src/components/proposals/tiptap-editor.tsx
frontend/src/components/ui/
frontend/src/components/ui/badge.tsx
frontend/src/components/ui/button.tsx
frontend/src/components/ui/card.tsx
frontend/src/components/ui/empty-state.tsx
frontend/src/components/ui/error-state.tsx
frontend/src/components/ui/input.tsx
frontend/src/components/ui/label.tsx
frontend/src/components/ui/loading-spinner.tsx
frontend/src/components/ui/textarea.tsx
frontend/src/lib/
frontend/src/lib/constants/
frontend/src/lib/constants/api-endpoints.ts
frontend/src/lib/constants/routes.ts
frontend/src/lib/stores/
frontend/src/lib/stores/auth-store.ts
frontend/src/lib/stores/proposal-store.ts
frontend/src/lib/utils/
frontend/src/lib/utils/cn.ts
frontend/src/lib/utils/format.ts
frontend/src/lib/utils/index.ts
frontend/src/types/
frontend/src/types/api.ts
frontend/src/types/grant.ts
frontend/src/types/organization.ts
frontend/src/types/proposal.ts
frontend/src/types/user.ts
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll help you design a comprehensive backend architecture for your decoupled React-Django application. Let me start by examining the existing documentation to understand the current architecture plan.

<read_file>
<args>
  <file>
    <path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
    <line_range>1-100</line_range>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'documentation/BACKEND_ARCHITECTURE_PLAN.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
<content lines="1-100">
  1 | # Django Backend Architecture Plan for GrantBridge
  2 | 
  3 | ## Executive Summary
  4 | 
  5 | This document outlines the complete backend architecture for GrantBridge, a decoupled AI-powered grant management platform. The backend will be built with Django + Django Ninja, serving as a pure API layer for the React frontend hosted on Vercel.
  6 | 
  7 | ---
  8 | 
  9 | ## 1. Communication & Security Architecture
 10 | 
 11 | ### 1.1 CORS Configuration
 12 | 
 13 | **Strategy:** Whitelist-based CORS for production security with development flexibility.
 14 | 
 15 | ```python
 16 | # config/settings/base.py
 17 | CORS_ALLOWED_ORIGINS = [
 18 |     "https://grantbridge.vercel.app",  # Production frontend
 19 |     "https://grantbridge-preview-*.vercel.app",  # Preview deployments
 20 | ]
 21 | 
 22 | # Development settings
 23 | CORS_ALLOW_CREDENTIALS = True
 24 | CORS_ALLOW_HEADERS = [
 25 |     'accept',
 26 |     'accept-encoding',
 27 |     'authorization',
 28 |     'content-type',
 29 |     'dnt',
 30 |     'origin',
 31 |     'user-agent',
 32 |     'x-csrftoken',
 33 |     'x-requested-with',
 34 | ]
 35 | ```
 36 | 
 37 | **Environment-based Configuration:**
 38 | - **Development:** `CORS_ALLOW_ALL_ORIGINS = True` for local testing
 39 | - **Staging/Production:** Explicit whitelist of Vercel domains
 40 | - **Dynamic Preview URLs:** Use regex pattern matching for Vercel preview deployments
 41 | 
 42 | ### 1.2 Authentication System
 43 | 
 44 | **Approach:** Stateless JWT Authentication (suitable for decoupled architecture)
 45 | 
 46 | **Library:** `django-ninja-jwt` (FastAPI-style JWT for Django Ninja)
 47 | 
 48 | **Token Strategy:**
 49 | - **Access Token:** Short-lived (15 minutes), used for API requests
 50 | - **Refresh Token:** Long-lived (7 days), stored securely, used to obtain new access tokens
 51 | - **Token Storage (Frontend):** 
 52 |   - Access token: Memory/state (not localStorage for security)
 53 |   - Refresh token: httpOnly cookie or secure localStorage
 54 | 
 55 | **Authentication Flow:**
 56 | 
 57 | ```mermaid
 58 | sequenceDiagram
 59 |     participant Frontend
 60 |     participant Backend
 61 |     participant Database
 62 |     
 63 |     Frontend->>Backend: POST /api/v1/auth/register
 64 |     Backend->>Database: Create User & Organization
 65 |     Backend-->>Frontend: {user, accessToken, refreshToken}
 66 |     
 67 |     Frontend->>Backend: POST /api/v1/auth/login
 68 |     Backend->>Database: Verify Credentials
 69 |     Backend-->>Frontend: {user, accessToken, refreshToken}
 70 |     
 71 |     Frontend->>Backend: GET /api/v1/grants (Authorization: Bearer token)
 72 |     Backend->>Backend: Validate JWT
 73 |     Backend->>Database: Fetch Grants
 74 |     Backend-->>Frontend: {grants[]}
 75 |     
 76 |     Frontend->>Backend: POST /api/v1/auth/refresh
 77 |     Backend->>Backend: Validate Refresh Token
 78 |     Backend-->>Frontend: {accessToken}
 79 | ```
 80 | 
 81 | **Security Features:**
 82 | - Password hashing: Django's built-in PBKDF2 (or Argon2)
 83 | - Rate limiting on auth endpoints (django-ratelimit)
 84 | - Token blacklisting for logout
 85 | - HTTPS-only in production
 86 | - Secure cookie flags (httpOnly, secure, sameSite)
 87 | 
 88 | ### 1.3 API Security Headers
 89 | 
 90 | ```python
 91 | SECURE_BROWSER_XSS_FILTER = True
 92 | SECURE_CONTENT_TYPE_NOSNIFF = True
 93 | X_FRAME_OPTIONS = 'DENY'
 94 | SECURE_SSL_REDIRECT = True  # Production only
 95 | SESSION_COOKIE_SECURE = True  # Production only
 96 | CSRF_COOKIE_SECURE = True  # Production only
 97 | ```
 98 | 
 99 | ---
100 | 
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
documentation\BACKEND_ARCHITECTURE_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/BACKEND_ARCHITECTURE_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:46:14.946Z
User time zone: Europe/Madrid, UTC+2:00

# Current Cost
$0.03

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<read_file>
<args>
  <file>
    <path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
    <line_range>100-300</line_range>
  </file>
  <file>
    <path>frontend/src/lib/constants/api-endpoints.ts</path>
  </file>
  <file>
    <path>frontend/src/types/user.ts</path>
  </file>
  <file>
    <path>frontend/src/types/grant.ts</path>
  </file>
  <file>
    <path>frontend/src/types/proposal.ts</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 5 files] Result:
<files>
<file><path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
<content lines="100-300">
100 | 
101 | ## 2. API Route Design
102 | 
103 | ### 2.1 API Structure Overview
104 | 
105 | **Base URL:** `/api/v1/`
106 | 
107 | **API Versioning Strategy:** URL-based versioning for clear contract management
108 | 
109 | ### 2.2 Complete Endpoint Mapping
110 | 
111 | #### 2.2.1 Authentication Endpoints
112 | 
113 | | Method | Endpoint | Description | Request Body | Response |
114 | |--------|----------|-------------|--------------|----------|
115 | | POST | `/auth/register` | Register new user & organization | `{name, email, password, organizationName?}` | `{user, accessToken, refreshToken}` |
116 | | POST | `/auth/login` | User login | `{email, password}` | `{user, accessToken, refreshToken}` |
117 | | POST | `/auth/refresh` | Refresh access token | `{refreshToken}` | `{accessToken}` |
118 | | POST | `/auth/logout` | Logout & blacklist token | `{refreshToken}` | `{message}` |
119 | | GET | `/auth/me` | Get current user | - | `{user}` |
120 | 
121 | #### 2.2.2 Organization Endpoints
122 | 
123 | | Method | Endpoint | Description | Auth Required | Response |
124 | |--------|----------|-------------|---------------|----------|
125 | | GET | `/organizations` | List all organizations (admin) | Yes | `{organizations[]}` |
126 | | GET | `/organizations/{id}` | Get organization details | Yes | `{organization}` |
127 | | PUT | `/organizations/{id}` | Update organization profile | Yes | `{organization}` |
128 | | PATCH | `/organizations/{id}` | Partial update organization | Yes | `{organization}` |
129 | | GET | `/organizations/{id}/stats` | Get organization statistics | Yes | `{stats}` |
130 | 
131 | **Organization Stats Response:**
132 | ```json
133 | {
134 |   "activeApplications": 12,
135 |   "totalFundingSought": 485000,
136 |   "matchRate": 87,
137 |   "proposalsDrafted": 24,
138 |   "approvedGrants": 8,
139 |   "pendingApplications": 4
140 | }
141 | ```
142 | 
143 | #### 2.2.3 Grant Endpoints
144 | 
145 | | Method | Endpoint | Description | Query Params | Response |
146 | |--------|----------|-------------|--------------|----------|
147 | | GET | `/grants` | List all grants with filters | `search, minAmount, maxAmount, tags[], status, sortBy, sortOrder, page, limit` | `{grants[], total, page, pages}` |
148 | | GET | `/grants/{id}` | Get grant details | - | `{grant}` |
149 | | POST | `/grants` | Create new grant (admin) | Grant object | `{grant}` |
150 | | PUT | `/grants/{id}` | Update grant | Grant object | `{grant}` |
151 | | DELETE | `/grants/{id}` | Delete grant (admin) | - | `{message}` |
152 | | GET | `/grants/search` | Semantic search grants | `q, limit` | `{grants[], scores[]}` |
153 | | POST | `/grants/{id}/save` | Save grant for later | - | `{message}` |
154 | | DELETE | `/grants/{id}/save` | Unsave grant | - | `{message}` |
155 | 
156 | **Grant List Response:**
157 | ```json
158 | {
159 |   "grants": [
160 |     {
161 |       "id": "grant-uuid",
162 |       "title": "Community Development Grant 2024",
163 |       "organization": "National Community Foundation",
164 |       "fundingAmount": 50000,
165 |       "deadline": "2024-03-15T23:59:59Z",
166 |       "requirements": "Must serve underserved communities...",
167 |       "tags": ["community", "development", "education"],
168 |       "source": "grants.gov",
169 |       "matchScore": 94,
170 |       "status": "new",
171 |       "description": "Supporting community-led initiatives...",
172 |       "eligibility": ["501(c)(3) status", "Operating for 2+ years"],
173 |       "createdAt": "2024-01-15T10:00:00Z",
174 |       "updatedAt": "2024-02-01T14:30:00Z"
175 |     }
176 |   ],
177 |   "total": 156,
178 |   "page": 1,
179 |   "pages": 16
180 | }
181 | ```
182 | 
183 | #### 2.2.4 Matching Endpoints
184 | 
185 | | Method | Endpoint | Description | Request Body | Response |
186 | |--------|----------|-------------|--------------|----------|
187 | | GET | `/matching` | Get matched grants for user's org | `limit, threshold` | `{matches[]}` |
188 | | GET | `/matching/{orgId}` | Get matches for specific org | `limit, threshold` | `{matches[]}` |
189 | | POST | `/matching/calculate` | Trigger match calculation | `{organizationId, grantIds[]}` | `{matches[]}` |
190 | 
191 | **Match Response:**
192 | ```json
193 | {
194 |   "matches": [
195 |     {
196 |       "grant": {},
197 |       "matchScore": 94,
198 |       "matchReasons": [
199 |         "Mission alignment: 95%",
200 |         "Category match: Community Development",
201 |         "Funding range appropriate"
202 |       ],
203 |       "recommendedActions": [
204 |         "Review eligibility requirements",
205 |         "Prepare project timeline",
206 |         "Draft initial proposal"
207 |       ]
208 |     }
209 |   ]
210 | }
211 | ```
212 | 
213 | #### 2.2.5 Proposal Endpoints
214 | 
215 | | Method | Endpoint | Description | Request Body | Response |
216 | |--------|----------|-------------|--------------|----------|
217 | | GET | `/proposals` | List user's proposals | `status, grantId, page, limit` | `{proposals[], total}` |
218 | | GET | `/proposals/{id}` | Get proposal details | - | `{proposal}` |
219 | | POST | `/proposals` | Create new proposal | `{grantId, title, content?}` | `{proposal}` |
220 | | PUT | `/proposals/{id}` | Update proposal | `{title?, content?, status?}` | `{proposal}` |
221 | | PATCH | `/proposals/{id}` | Partial update | Partial proposal | `{proposal}` |
222 | | DELETE | `/proposals/{id}` | Delete proposal | - | `{message}` |
223 | | POST | `/proposals/{id}/submit` | Submit proposal | - | `{proposal, message}` |
224 | | GET | `/proposals/{id}/export` | Export as PDF/DOCX | `format` | File download |
225 | 
226 | #### 2.2.6 AI Service Endpoints
227 | 
228 | | Method | Endpoint | Description | Request Body | Response |
229 | |--------|----------|-------------|--------------|----------|
230 | | POST | `/ai/generate-proposal` | Generate proposal draft | `{grantId, organizationId, tone?}` | `{content, metadata}` |
231 | | POST | `/ai/improve-text` | Improve selected text | `{text, action, tone?}` | `{improvedText, suggestions[]}` |
232 | | POST | `/ai/rewrite` | Rewrite text | `{text, tone, style}` | `{rewrittenText}` |
233 | | POST | `/ai/adjust-tone` | Adjust text tone | `{text, targetTone}` | `{adjustedText}` |
234 | | POST | `/ai/summarize` | Summarize text | `{text, maxLength}` | `{summary}` |
235 | | POST | `/ai/expand` | Expand text | `{text, targetLength}` | `{expandedText}` |
236 | 
237 | **AI Generation Request:**
238 | ```json
239 | {
240 |   "grantId": "grant-uuid",
241 |   "organizationId": "org-uuid",
242 |   "tone": "professional",
243 |   "sections": ["executive_summary", "project_description", "budget_narrative"]
244 | }
245 | ```
246 | 
247 | **AI Generation Response:**
248 | ```json
249 | {
250 |   "content": "# Executive Summary\n\nOur organization...",
251 |   "metadata": {
252 |     "model": "watsonx.ai/granite-13b",
253 |     "generatedAt": "2024-02-15T10:30:00Z",
254 |     "tokensUsed": 1250,
255 |     "confidence": 0.92
256 |   },
257 |   "suggestions": [
258 |     "Consider adding specific metrics",
259 |     "Include community impact data"
260 |   ]
261 | }
262 | ```
263 | 
264 | #### 2.2.7 Dashboard Endpoints
265 | 
266 | | Method | Endpoint | Description | Query Params | Response |
267 | |--------|----------|-------------|--------------|----------|
268 | | GET | `/dashboard/stats` | Get dashboard statistics | `period` | `{stats}` |
269 | | GET | `/dashboard/analytics` | Get analytics data | `startDate, endDate` | `{analytics}` |
270 | | GET | `/dashboard/notifications` | Get user notifications | `unread, limit` | `{notifications[]}` |
271 | | PUT | `/dashboard/notifications/{id}/read` | Mark notification as read | - | `{notification}` |
272 | 
273 | **Dashboard Stats Response:**
274 | ```json
275 | {
276 |   "activeApplications": 12,
277 |   "totalFundingSought": 485000,
278 |   "matchRate": 87,
279 |   "proposalsDrafted": 24,
280 |   "trends": {
281 |     "applications": "+12%",
282 |     "funding": "+8%",
283 |     "matchRate": "+5%",
284 |     "proposals": "+18%"
285 |   },
286 |   "recentActivity": [
287 |     {
288 |       "type": "grant_matched",
289 |       "title": "New grant match",
290 |       "message": "Community Development Grant matches your profile",
291 |       "timestamp": "2024-02-15T09:30:00Z"
292 |     }
293 |   ]
294 | }
295 | ```
296 | 
297 | #### 2.2.8 Analytics Endpoints
298 | 
299 | | Method | Endpoint | Description | Query Params | Response |
300 | |--------|----------|-------------|--------------|----------|
</content>
</file>
<file><path>frontend/src/lib/constants/api-endpoints.ts</path>
<content lines="1-53">
 1 | const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
 2 | 
 3 | export const API_ENDPOINTS = {
 4 |   // Authentication
 5 |   AUTH: {
 6 |     LOGIN: `${API_BASE}/auth/login`,
 7 |     REGISTER: `${API_BASE}/auth/register`,
 8 |     REFRESH: `${API_BASE}/auth/refresh`,
 9 |     LOGOUT: `${API_BASE}/auth/logout`,
10 |   },
11 |   
12 |   // Organizations
13 |   ORGANIZATIONS: {
14 |     BASE: `${API_BASE}/organizations`,
15 |     BY_ID: (id: string) => `${API_BASE}/organizations/${id}`,
16 |   },
17 |   
18 |   // Grants
19 |   GRANTS: {
20 |     BASE: `${API_BASE}/grants`,
21 |     BY_ID: (id: string) => `${API_BASE}/grants/${id}`,
22 |     SEARCH: `${API_BASE}/grants/search`,
23 |   },
24 |   
25 |   // Matching
26 |   MATCHING: {
27 |     BASE: `${API_BASE}/matching`,
28 |     BY_ORG: (orgId: string) => `${API_BASE}/matching/${orgId}`,
29 |   },
30 |   
31 |   // Proposals
32 |   PROPOSALS: {
33 |     BASE: `${API_BASE}/proposals`,
34 |     BY_ID: (id: string) => `${API_BASE}/proposals/${id}`,
35 |   },
36 |   
37 |   // AI Services
38 |   AI: {
39 |     GENERATE_PROPOSAL: `${API_BASE}/ai/generate-proposal`,
40 |     IMPROVE_TEXT: `${API_BASE}/ai/improve-text`,
41 |     REWRITE: `${API_BASE}/ai/rewrite`,
42 |     ADJUST_TONE: `${API_BASE}/ai/adjust-tone`,
43 |   },
44 |   
45 |   // Dashboard
46 |   DASHBOARD: {
47 |     STATS: `${API_BASE}/dashboard/stats`,
48 |   },
49 | } as const
50 | 
51 | export default API_ENDPOINTS
52 | 
53 | // Made with Bob
</content>
</file>
<file><path>frontend/src/types/user.ts</path>
<content lines="1-28">
 1 | export interface User {
 2 |   id: string
 3 |   email: string
 4 |   name: string
 5 |   organizationId: string
 6 |   role: 'admin' | 'member'
 7 |   createdAt: string
 8 | }
 9 | 
10 | export interface AuthResponse {
11 |   user: User
12 |   token: string
13 |   refreshToken?: string
14 | }
15 | 
16 | export interface LoginCredentials {
17 |   email: string
18 |   password: string
19 | }
20 | 
21 | export interface RegisterData {
22 |   name: string
23 |   email: string
24 |   password: string
25 |   organizationName?: string
26 | }
27 | 
28 | // Made with Bob
</content>
</file>
<file><path>frontend/src/types/grant.ts</path>
<content lines="1-34">
 1 | export type GrantStatus = 'opportunity' | 'reviewing' | 'drafting' | 'submitted'
 2 | 
 3 | export interface Grant {
 4 |   id: string
 5 |   title: string
 6 |   fundingAmount: number
 7 |   requirements: string
 8 |   deadline: string
 9 |   tags: string[]
10 |   source: string
11 |   matchScore?: number
12 |   status: GrantStatus
13 |   description?: string
14 |   eligibility?: string[]
15 |   createdAt: string
16 |   updatedAt?: string
17 | }
18 | 
19 | export interface GrantFilters {
20 |   search?: string
21 |   minAmount?: number
22 |   maxAmount?: number
23 |   tags?: string[]
24 |   status?: GrantStatus
25 |   sortBy?: 'matchScore' | 'deadline' | 'fundingAmount'
26 |   sortOrder?: 'asc' | 'desc'
27 | }
28 | 
29 | export interface GrantUpdateData {
30 |   status?: GrantStatus
31 |   matchScore?: number
32 | }
33 | 
34 | // Made with Bob
</content>
</file>
<file><path>frontend/src/types/proposal.ts</path>
<content lines="1-33">
 1 | export type ProposalStatus = 'draft' | 'review' | 'submitted'
 2 | 
 3 | export interface Proposal {
 4 |   id: string
 5 |   grantId: string
 6 |   organizationId: string
 7 |   title: string
 8 |   content: string
 9 |   status: ProposalStatus
10 |   aiGenerated: boolean
11 |   createdAt: string
12 |   updatedAt: string
13 | }
14 | 
15 | export interface ProposalGenerationParams {
16 |   grantId: string
17 |   organizationId: string
18 |   tone?: 'professional' | 'persuasive' | 'concise'
19 | }
20 | 
21 | export interface ProposalUpdateData {
22 |   title?: string
23 |   content?: string
24 |   status?: ProposalStatus
25 | }
26 | 
27 | export interface AIImprovementParams {
28 |   text: string
29 |   action: 'rewrite' | 'expand' | 'shorten' | 'improve'
30 |   tone?: 'professional' | 'persuasive' | 'concise'
31 | }
32 | 
33 | // Made with Bob
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
documentation\BACKEND_ARCHITECTURE_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/BACKEND_ARCHITECTURE_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:46:23.607Z
User time zone: Europe/Madrid, UTC+2:00

# Current Cost
$0.07

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<read_file>
<args>
  <file>
    <path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
    <line_range>300-500</line_range>
  </file>
  <file>
    <path>frontend/src/types/organization.ts</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'documentation/BACKEND_ARCHITECTURE_PLAN.md', 'frontend/src/types/organization.ts'] Result:
<files>
<file><path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
<content lines="300-500">
300 | |--------|----------|-------------|--------------|----------|
301 | | GET | `/analytics/trends` | Application trends over time | `startDate, endDate, groupBy` | `{trends[]}` |
302 | | GET | `/analytics/categories` | Grant category distribution | - | `{categories[]}` |
303 | | GET | `/analytics/success-rate` | Success rate by category | - | `{rates[]}` |
304 | | GET | `/analytics/funding` | Funding amount trends | `startDate, endDate` | `{funding[]}` |
305 | 
306 | ### 2.3 API Response Standards
307 | 
308 | **Success Response Format:**
309 | ```json
310 | {
311 |   "data": {},
312 |   "message": "Success message",
313 |   "timestamp": "2024-02-15T10:30:00Z"
314 | }
315 | ```
316 | 
317 | **Error Response Format:**
318 | ```json
319 | {
320 |   "error": {
321 |     "code": "VALIDATION_ERROR",
322 |     "message": "Invalid request parameters",
323 |     "details": {
324 |       "email": ["This field is required"],
325 |       "password": ["Password must be at least 8 characters"]
326 |     }
327 |   },
328 |   "timestamp": "2024-02-15T10:30:00Z"
329 | }
330 | ```
331 | 
332 | **Pagination Format:**
333 | ```json
334 | {
335 |   "data": [],
336 |   "pagination": {
337 |     "page": 1,
338 |     "limit": 20,
339 |     "total": 156,
340 |     "pages": 8,
341 |     "hasNext": true,
342 |     "hasPrev": false
343 |   }
344 | }
345 | ```
346 | 
347 | ---
348 | 
349 | ## 3. Data Models Schema
350 | 
351 | ### 3.1 Core Models Overview
352 | 
353 | The backend requires the following models to replace frontend mock data:
354 | 
355 | 1. **User** - Authentication and user management
356 | 2. **Organization** - NGO profiles with mission, goals, categories
357 | 3. **Grant** - Grant opportunities with requirements and deadlines
358 | 4. **Proposal** - AI-generated and user-edited proposals
359 | 5. **GrantMatch** - Matching scores between organizations and grants
360 | 6. **Notification** - User notifications for various events
361 | 7. **Application** - Grant application tracking
362 | 
363 | ### 3.2 Detailed Model Definitions
364 | 
365 | #### 3.2.1 User Model
366 | 
367 | ```python
368 | # apps/authentication/models.py
369 | from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
370 | from django.db import models
371 | import uuid
372 | 
373 | class User(AbstractBaseUser, PermissionsMixin):
374 |     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
375 |     email = models.EmailField(unique=True, db_index=True)
376 |     name = models.CharField(max_length=255)
377 |     organization = models.ForeignKey(
378 |         'organizations.Organization',
379 |         on_delete=models.CASCADE,
380 |         related_name='users'
381 |     )
382 |     role = models.CharField(
383 |         max_length=20,
384 |         choices=[('admin', 'Admin'), ('member', 'Member')],
385 |         default='member'
386 |     )
387 |     is_active = models.BooleanField(default=True)
388 |     is_staff = models.BooleanField(default=False)
389 |     created_at = models.DateTimeField(auto_now_add=True)
390 |     updated_at = models.DateTimeField(auto_now=True)
391 |     last_login = models.DateTimeField(null=True, blank=True)
392 |     
393 |     USERNAME_FIELD = 'email'
394 |     REQUIRED_FIELDS = ['name']
395 |     
396 |     class Meta:
397 |         db_table = 'users'
398 |         indexes = [
399 |             models.Index(fields=['email']),
400 |             models.Index(fields=['organization', 'role']),
401 |         ]
402 | ```
403 | 
404 | #### 3.2.2 Organization Model
405 | 
406 | ```python
407 | # apps/organizations/models.py
408 | from django.db import models
409 | import uuid
410 | 
411 | class Organization(models.Model):
412 |     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
413 |     name = models.CharField(max_length=255, db_index=True)
414 |     type = models.CharField(max_length=100, default='501(c)(3) Nonprofit')
415 |     ein = models.CharField(max_length=20, unique=True, null=True, blank=True)
416 |     
417 |     # Contact Information
418 |     email = models.EmailField()
419 |     phone = models.CharField(max_length=20, blank=True)
420 |     website = models.URLField(blank=True)
421 |     
422 |     # Address
423 |     address = models.CharField(max_length=255, blank=True)
424 |     city = models.CharField(max_length=100, blank=True)
425 |     state = models.CharField(max_length=50, blank=True)
426 |     zip_code = models.CharField(max_length=10, blank=True)
427 |     country = models.CharField(max_length=100, default='USA')
428 |     
429 |     # Organization Details (matches frontend types)
430 |     mission = models.TextField(help_text="Organization's mission statement")
431 |     description = models.TextField(blank=True)
432 |     goals = models.JSONField(default=list, help_text="List of organizational goals")
433 |     categories = models.JSONField(default=list, help_text="Nonprofit categories/focus areas")
434 |     historical_projects = models.JSONField(default=list, help_text="Past projects")
435 |     
436 |     # Financial
437 |     year_founded = models.IntegerField(null=True, blank=True)
438 |     annual_budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
439 |     funding_needs = models.DecimalField(max_digits=12, decimal_places=2, default=0)
440 |     
441 |     # Metadata
442 |     is_verified = models.BooleanField(default=False)
443 |     created_at = models.DateTimeField(auto_now_add=True)
444 |     updated_at = models.DateTimeField(auto_now=True)
445 |     
446 |     # AI/Matching
447 |     embedding_vector = models.JSONField(null=True, blank=True)
448 |     last_embedding_update = models.DateTimeField(null=True, blank=True)
449 |     
450 |     class Meta:
451 |         db_table = 'organizations'
452 |         indexes = [
453 |             models.Index(fields=['name']),
454 |             models.Index(fields=['created_at']),
455 |         ]
456 | ```
457 | 
458 | #### 3.2.3 Grant Model
459 | 
460 | ```python
461 | # apps/grants/models.py
462 | from django.db import models
463 | import uuid
464 | 
465 | class Grant(models.Model):
466 |     STATUS_CHOICES = [
467 |         ('opportunity', 'Opportunity'),
468 |         ('reviewing', 'Reviewing'),
469 |         ('drafting', 'Drafting'),
470 |         ('submitted', 'Submitted'),
471 |     ]
472 |     
473 |     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
474 |     title = models.CharField(max_length=500, db_index=True)
475 |     organization = models.CharField(max_length=255, help_text="Funding organization")
476 |     
477 |     # Financial
478 |     funding_amount = models.DecimalField(max_digits=12, decimal_places=2)
479 |     min_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
480 |     max_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
481 |     
482 |     # Details
483 |     description = models.TextField()
484 |     requirements = models.TextField(help_text="Grant requirements and criteria")
485 |     eligibility = models.JSONField(default=list, help_text="Eligibility criteria")
486 |     
487 |     # Categorization
488 |     tags = models.JSONField(default=list, help_text="Grant tags/keywords")
489 |     categories = models.JSONField(default=list, help_text="Grant categories")
490 |     
491 |     # Dates
492 |     deadline = models.DateTimeField(db_index=True)
493 |     announcement_date = models.DateTimeField(null=True, blank=True)
494 |     award_date = models.DateTimeField(null=True, blank=True)
495 |     
496 |     # Source
497 |     source = models.CharField(max_length=255, help_text="Source (e.g., grants.gov)")
498 |     source_url = models.URLField(blank=True)
499 |     external_id = models.CharField(max_length=255, blank=True, db_index=True)
500 |     
</content>
</file>
<file><path>frontend/src/types/organization.ts</path>
<content lines="1-22">
 1 | export interface Organization {
 2 |   id: string
 3 |   name: string
 4 |   mission: string
 5 |   goals: string[]
 6 |   categories: string[]
 7 |   historicalProjects: string[]
 8 |   fundingNeeds: number
 9 |   createdAt: string
10 |   updatedAt: string
11 | }
12 | 
13 | export interface OrganizationUpdateData {
14 |   name?: string
15 |   mission?: string
16 |   goals?: string[]
17 |   categories?: string[]
18 |   historicalProjects?: string[]
19 |   fundingNeeds?: number
20 | }
21 | 
22 | // Made with Bob
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
documentation\BACKEND_ARCHITECTURE_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/BACKEND_ARCHITECTURE_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:46:45.822Z
User time zone: Europe/Madrid, UTC+2:00

# Current Cost
$0.12

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<read_file>
<args>
  <file>
    <path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
    <line_range>500-700</line_range>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'documentation/BACKEND_ARCHITECTURE_PLAN.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
<content lines="500-700">
500 |     
501 |     # Status
502 |     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='opportunity')
503 |     is_active = models.BooleanField(default=True, db_index=True)
504 |     
505 |     # AI/Matching
506 |     embedding_vector = models.JSONField(null=True, blank=True)
507 |     last_embedding_update = models.DateTimeField(null=True, blank=True)
508 |     
509 |     # Metadata
510 |     created_at = models.DateTimeField(auto_now_add=True)
511 |     updated_at = models.DateTimeField(auto_now=True)
512 |     
513 |     class Meta:
514 |         db_table = 'grants'
515 |         indexes = [
516 |             models.Index(fields=['deadline', 'is_active']),
517 |             models.Index(fields=['funding_amount']),
518 |             models.Index(fields=['created_at']),
519 |         ]
520 |         ordering = ['-deadline']
521 | ```
522 | 
523 | #### 3.2.4 Proposal Model
524 | 
525 | ```python
526 | # apps/proposals/models.py
527 | from django.db import models
528 | import uuid
529 | 
530 | class Proposal(models.Model):
531 |     STATUS_CHOICES = [
532 |         ('draft', 'Draft'),
533 |         ('review', 'Under Review'),
534 |         ('submitted', 'Submitted'),
535 |         ('approved', 'Approved'),
536 |         ('rejected', 'Rejected'),
537 |     ]
538 |     
539 |     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
540 |     grant = models.ForeignKey('grants.Grant', on_delete=models.CASCADE, related_name='proposals')
541 |     organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='proposals')
542 |     created_by = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, related_name='created_proposals')
543 |     
544 |     # Content
545 |     title = models.CharField(max_length=500)
546 |     content = models.TextField(help_text="Proposal content in markdown/HTML")
547 |     
548 |     # Status
549 |     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
550 |     
551 |     # AI Generation
552 |     ai_generated = models.BooleanField(default=False)
553 |     ai_model_used = models.CharField(max_length=100, blank=True)
554 |     generation_metadata = models.JSONField(null=True, blank=True)
555 |     
556 |     # Submission
557 |     submitted_at = models.DateTimeField(null=True, blank=True)
558 |     submission_method = models.CharField(max_length=100, blank=True)
559 |     
560 |     # Versioning
561 |     version = models.IntegerField(default=1)
562 |     parent_version = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='versions')
563 |     
564 |     # Metadata
565 |     created_at = models.DateTimeField(auto_now_add=True)
566 |     updated_at = models.DateTimeField(auto_now=True)
567 |     
568 |     class Meta:
569 |         db_table = 'proposals'
570 |         indexes = [
571 |             models.Index(fields=['organization', 'status']),
572 |             models.Index(fields=['grant', 'status']),
573 |             models.Index(fields=['created_at']),
574 |         ]
575 |         ordering = ['-updated_at']
576 | ```
577 | 
578 | #### 3.2.5 GrantMatch Model
579 | 
580 | ```python
581 | # apps/matching/models.py
582 | from django.db import models
583 | import uuid
584 | 
585 | class GrantMatch(models.Model):
586 |     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
587 |     organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='grant_matches')
588 |     grant = models.ForeignKey('grants.Grant', on_delete=models.CASCADE, related_name='organization_matches')
589 |     
590 |     # Matching Score
591 |     match_score = models.FloatField(db_index=True, help_text="0-100 compatibility score")
592 |     
593 |     # Match Details
594 |     match_reasons = models.JSONField(default=list, help_text="List of reasons for match")
595 |     recommended_actions = models.JSONField(default=list, help_text="Suggested next steps")
596 |     
597 |     # Match Metadata
598 |     algorithm_version = models.CharField(max_length=50, default='v1.0')
599 |     calculated_at = models.DateTimeField(auto_now_add=True)
600 |     
601 |     # User Interaction
602 |     is_saved = models.BooleanField(default=False)
603 |     is_dismissed = models.BooleanField(default=False)
604 |     viewed_at = models.DateTimeField(null=True, blank=True)
605 |     
606 |     class Meta:
607 |         db_table = 'grant_matches'
608 |         unique_together = [['organization', 'grant']]
609 |         indexes = [
610 |             models.Index(fields=['organization', 'match_score']),
611 |             models.Index(fields=['grant', 'match_score']),
612 |             models.Index(fields=['-match_score']),
613 |         ]
614 |         ordering = ['-match_score']
615 | ```
616 | 
617 | #### 3.2.6 Notification Model
618 | 
619 | ```python
620 | # apps/core/models.py
621 | from django.db import models
622 | import uuid
623 | 
624 | class Notification(models.Model):
625 |     TYPE_CHOICES = [
626 |         ('grant_matched', 'Grant Matched'),
627 |         ('application_approved', 'Application Approved'),
628 |         ('application_rejected', 'Application Rejected'),
629 |         ('deadline_reminder', 'Deadline Reminder'),
630 |         ('proposal_generated', 'Proposal Generated'),
631 |         ('system', 'System Notification'),
632 |     ]
633 |     
634 |     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
635 |     user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='notifications')
636 |     
637 |     type = models.CharField(max_length=50, choices=TYPE_CHOICES)
638 |     title = models.CharField(max_length=255)
639 |     message = models.TextField()
640 |     
641 |     # Links
642 |     link_url = models.CharField(max_length=500, blank=True)
643 |     related_grant = models.ForeignKey('grants.Grant', on_delete=models.SET_NULL, null=True, blank=True)
644 |     related_proposal = models.ForeignKey('proposals.Proposal', on_delete=models.SET_NULL, null=True, blank=True)
645 |     
646 |     # Status
647 |     is_read = models.BooleanField(default=False, db_index=True)
648 |     read_at = models.DateTimeField(null=True, blank=True)
649 |     
650 |     created_at = models.DateTimeField(auto_now_add=True)
651 |     
652 |     class Meta:
653 |         db_table = 'notifications'
654 |         indexes = [
655 |             models.Index(fields=['user', 'is_read']),
656 |             models.Index(fields=['-created_at']),
657 |         ]
658 |         ordering = ['-created_at']
659 | ```
660 | 
661 | #### 3.2.7 Application Model (for tracking)
662 | 
663 | ```python
664 | # apps/grants/models.py
665 | class Application(models.Model):
666 |     STATUS_CHOICES = [
667 |         ('draft', 'Draft'),
668 |         ('submitted', 'Submitted'),
669 |         ('under_review', 'Under Review'),
670 |         ('approved', 'Approved'),
671 |         ('rejected', 'Rejected'),
672 |     ]
673 |     
674 |     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
675 |     grant = models.ForeignKey('Grant', on_delete=models.CASCADE, related_name='applications')
676 |     organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='applications')
677 |     proposal = models.OneToOneField('proposals.Proposal', on_delete=models.SET_NULL, null=True, blank=True)
678 |     
679 |     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
680 |     progress = models.IntegerField(default=0, help_text="Completion percentage 0-100")
681 |     
682 |     submitted_date = models.DateTimeField(null=True, blank=True)
683 |     
684 |     created_at = models.DateTimeField(auto_now_add=True)
685 |     updated_at = models.DateTimeField(auto_now=True)
686 |     
687 |     class Meta:
688 |         db_table = 'applications'
689 |         indexes = [
690 |             models.Index(fields=['organization', 'status']),
691 |             models.Index(fields=['grant', 'status']),
692 |         ]
693 | ```
694 | 
695 | ### 3.3 Model Relationships Diagram
696 | 
697 | ```mermaid
698 | erDiagram
699 |     User ||--o{ Proposal : creates
700 |     User }o--|| Organization : belongs_to
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
documentation\BACKEND_ARCHITECTURE_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/BACKEND_ARCHITECTURE_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:46:50.600Z
User time zone: Europe/Madrid, UTC+2:00

# Current Cost
$0.18

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<read_file>
<args>
  <file>
    <path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
    <line_range>700-900</line_range>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'documentation/BACKEND_ARCHITECTURE_PLAN.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
<content lines="700-900">
700 |     User }o--|| Organization : belongs_to
701 |     User ||--o{ Notification : receives
702 |     
703 |     Organization ||--o{ Proposal : submits
704 |     Organization ||--o{ GrantMatch : has
705 |     Organization ||--o{ Application : submits
706 |     
707 |     Grant ||--o{ Proposal : receives
708 |     Grant ||--o{ GrantMatch : matched_with
709 |     Grant ||--o{ Application : receives
710 |     
711 |     Proposal }o--|| Grant : for
712 |     Proposal }o--|| Organization : from
713 |     
714 |     Application }o--|| Grant : for
715 |     Application }o--|| Organization : from
716 |     Application }o--o| Proposal : includes
717 |     
718 |     GrantMatch }o--|| Organization : for
719 |     GrantMatch }o--|| Grant : matches
720 |     
721 |     Notification }o--|| User : notifies
722 |     Notification }o--o| Grant : about
723 |     Notification }o--o| Proposal : about
724 | ```
725 | 
726 | ---
727 | 
728 | ## 4. AI Service Layer Architecture
729 | 
730 | ### 4.1 AI Service Structure
731 | 
732 | ```
733 | apps/ai/
734 | ├── __init__.py
735 | ├── services/
736 | │   ├── __init__.py
737 | │   ├── base.py              # Base AI service class
738 | │   ├── matching.py          # Grant matching service
739 | │   ├── generation.py        # Proposal generation service
740 | │   ├── improvement.py       # Text improvement service
741 | │   └── embeddings.py        # Vector embedding service
742 | ├── providers/
743 | │   ├── __init__.py
744 | │   ├── base.py              # Base provider interface
745 | │   ├── watsonx.py           # IBM watsonx.ai provider
746 | │   ├── openai.py            # OpenAI provider (optional)
747 | │   └── anthropic.py         # Anthropic provider (optional)
748 | ├── prompts/
749 | │   ├── __init__.py
750 | │   ├── matching/
751 | │   │   ├── system.txt
752 | │   │   └── user_template.txt
753 | │   ├── generation/
754 | │   │   ├── executive_summary.txt
755 | │   │   ├── project_description.txt
756 | │   │   └── budget_narrative.txt
757 | │   └── improvement/
758 | │       ├── rewrite.txt
759 | │       ├── expand.txt
760 | │       └── tone_adjust.txt
761 | └── pipelines/
762 |     ├── __init__.py
763 |     ├── matching_pipeline.py
764 |     └── generation_pipeline.py
765 | ```
766 | 
767 | ### 4.2 Key AI Services
768 | 
769 | #### Grant Matching Service
770 | - Semantic similarity between organization mission and grant requirements
771 | - Category-based matching
772 | - Funding range compatibility
773 | - Historical project relevance
774 | 
775 | #### Proposal Generation Service
776 | - Executive summary generation
777 | - Project description drafting
778 | - Budget narrative creation
779 | - Organizational capacity section
780 | 
781 | #### Text Improvement Service
782 | - Rewrite for clarity
783 | - Tone adjustment (professional, persuasive, concise)
784 | - Text expansion
785 | - Summarization
786 | 
787 | ### 4.3 Vector Store Integration
788 | 
789 | **Technology:** ChromaDB or FAISS
790 | 
791 | **Purpose:**
792 | - Store embeddings for organizations and grants
793 | - Enable semantic search
794 | - Fast similarity matching
795 | 
796 | ---
797 | 
798 | ## 5. Infrastructure & Deployment Strategy
799 | 
800 | ### 5.1 Deployment Architecture
801 | 
802 | ```mermaid
803 | graph TB
804 |     subgraph "Frontend - Vercel"
805 |         A[React App]
806 |     end
807 |     
808 |     subgraph "Backend - Railway/Render"
809 |         B[Django + Nginx]
810 |         C[Celery Workers]
811 |         D[Redis]
812 |     end
813 |     
814 |     subgraph "Database - Neon/Supabase"
815 |         E[PostgreSQL]
816 |     end
817 |     
818 |     subgraph "AI Services"
819 |         F[watsonx.ai]
820 |         G[ChromaDB/FAISS]
821 |     end
822 |     
823 |     subgraph "Storage"
824 |         H[Cloudinary/S3]
825 |     end
826 |     
827 |     A -->|HTTPS/JWT| B
828 |     B --> E
829 |     B --> D
830 |     C --> D
831 |     C --> E
832 |     B --> F
833 |     B --> G
834 |     B --> H
835 | ```
836 | 
837 | ### 5.2 Platform Recommendations
838 | 
839 | #### Option 1: Railway (Recommended for PoC)
840 | 
841 | **Pros:**
842 | - Simple deployment from GitHub
843 | - Built-in PostgreSQL
844 | - Environment variable management
845 | - Automatic HTTPS
846 | - Free tier available
847 | 
848 | **Configuration:**
849 | ```yaml
850 | # railway.json
851 | {
852 |   "build": {
853 |     "builder": "NIXPACKS",
854 |     "buildCommand": "pip install -r requirements.txt && python manage.py collectstatic --noinput"
855 |   },
856 |   "deploy": {
857 |     "startCommand": "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT",
858 |     "healthcheckPath": "/api/v1/health",
859 |     "restartPolicyType": "ON_FAILURE"
860 |   }
861 | }
862 | ```
863 | 
864 | #### Option 2: Render
865 | 
866 | **Pros:**
867 | - Free tier with PostgreSQL
868 | - Auto-deploy from Git
869 | - Background workers support
870 | - Good documentation
871 | 
872 | **Configuration:**
873 | ```yaml
874 | # render.yaml
875 | services:
876 |   - type: web
877 |     name: grantbridge-api
878 |     env: python
879 |     buildCommand: "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"
880 |     startCommand: "gunicorn config.wsgi:application"
881 |     envVars:
882 |       - key: PYTHON_VERSION
883 |         value: 3.11
884 |       - key: DATABASE_URL
885 |         fromDatabase:
886 |           name: grantbridge-db
887 |           property: connectionString
888 |   
889 |   - type: worker
890 |     name: grantbridge-celery
891 |     env: python
892 |     buildCommand: "pip install -r requirements.txt"
893 |     startCommand: "celery -A config worker -l info"
894 |   
895 | databases:
896 |   - name: grantbridge-db
897 |     databaseName: grantbridge
898 |     user: grantbridge
899 | ```
900 | 
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
documentation\BACKEND_ARCHITECTURE_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/BACKEND_ARCHITECTURE_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:46:53.709Z
User time zone: Europe/Madrid, UTC+2:00

# Current Cost
$0.24

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<read_file>
<args>
  <file>
    <path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
    <line_range>900-1100</line_range>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'documentation/BACKEND_ARCHITECTURE_PLAN.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
<content lines="900-1100">
 900 | 
 901 | ### 5.3 Database Hosting
 902 | 
 903 | #### Recommended: Neon PostgreSQL
 904 | 
 905 | **Pros:**
 906 | - Serverless PostgreSQL
 907 | - Generous free tier
 908 | - Automatic backups
 909 | - Branch databases for testing
 910 | 
 911 | **Connection:**
 912 | ```python
 913 | # config/settings/production.py
 914 | DATABASES = {
 915 |     'default': {
 916 |         'ENGINE': 'django.db.backends.postgresql',
 917 |         'NAME': os.getenv('PGDATABASE'),
 918 |         'USER': os.getenv('PGUSER'),
 919 |         'PASSWORD': os.getenv('PGPASSWORD'),
 920 |         'HOST': os.getenv('PGHOST'),
 921 |         'PORT': os.getenv('PGPORT', 5432),
 922 |         'OPTIONS': {
 923 |             'sslmode': 'require',
 924 |         },
 925 |     }
 926 | }
 927 | ```
 928 | 
 929 | ### 5.4 Environment Variables Configuration
 930 | 
 931 | #### Backend Environment Variables
 932 | 
 933 | ```bash
 934 | # Django Settings
 935 | DJANGO_SECRET_KEY=your-secret-key-here
 936 | DJANGO_DEBUG=False
 937 | DJANGO_ALLOWED_HOSTS=grantbridge-api.railway.app,grantbridge-api.onrender.com
 938 | DJANGO_SETTINGS_MODULE=config.settings.production
 939 | 
 940 | # Database
 941 | DATABASE_URL=postgresql://user:password@host:5432/dbname
 942 | PGHOST=your-neon-host.neon.tech
 943 | PGDATABASE=grantbridge
 944 | PGUSER=your-user
 945 | PGPASSWORD=your-password
 946 | PGPORT=5432
 947 | 
 948 | # CORS
 949 | CORS_ALLOWED_ORIGINS=https://grantbridge.vercel.app,https://grantbridge-*.vercel.app
 950 | 
 951 | # JWT
 952 | JWT_SECRET_KEY=your-jwt-secret
 953 | JWT_ACCESS_TOKEN_LIFETIME=15  # minutes
 954 | JWT_REFRESH_TOKEN_LIFETIME=10080  # 7 days in minutes
 955 | 
 956 | # Redis (for Celery)
 957 | REDIS_URL=redis://default:password@host:6379
 958 | 
 959 | # AI Services
 960 | WATSONX_API_KEY=your-watsonx-api-key
 961 | WATSONX_PROJECT_ID=your-project-id
 962 | WATSONX_URL=https://us-south.ml.cloud.ibm.com
 963 | 
 964 | # Vector Store
 965 | VECTOR_STORE_PATH=/app/vector_store
 966 | CHROMA_PERSIST_DIRECTORY=/app/chroma_db
 967 | 
 968 | # File Storage (Optional)
 969 | CLOUDINARY_CLOUD_NAME=your-cloud-name
 970 | CLOUDINARY_API_KEY=your-api-key
 971 | CLOUDINARY_API_SECRET=your-api-secret
 972 | 
 973 | # Email (Optional)
 974 | EMAIL_HOST=smtp.sendgrid.net
 975 | EMAIL_PORT=587
 976 | EMAIL_HOST_USER=apikey
 977 | EMAIL_HOST_PASSWORD=your-sendgrid-api-key
 978 | DEFAULT_FROM_EMAIL=noreply@grantbridge.org
 979 | 
 980 | # Monitoring (Optional)
 981 | SENTRY_DSN=your-sentry-dsn
 982 | ```
 983 | 
 984 | #### Frontend Environment Variables (Vercel)
 985 | 
 986 | ```bash
 987 | # .env.production
 988 | NEXT_PUBLIC_API_URL=https://grantbridge-api.railway.app/api/v1
 989 | NEXT_PUBLIC_APP_NAME=GrantBridge
 990 | NEXT_PUBLIC_APP_URL=https://grantbridge.vercel.app
 991 | ```
 992 | 
 993 | ### 5.5 Deployment Workflow
 994 | 
 995 | ```mermaid
 996 | sequenceDiagram
 997 |     participant Dev as Developer
 998 |     participant Git as GitHub
 999 |     participant Railway as Railway/Render
1000 |     participant Vercel as Vercel
1001 |     participant DB as Neon PostgreSQL
1002 |     
1003 |     Dev->>Git: Push to main branch
1004 |     Git->>Railway: Trigger deployment
1005 |     Railway->>Railway: Build Docker image
1006 |     Railway->>Railway: Run migrations
1007 |     Railway->>DB: Apply schema changes
1008 |     Railway->>Railway: Collect static files
1009 |     Railway->>Railway: Start gunicorn
1010 |     Railway-->>Dev: Deployment complete
1011 |     
1012 |     Git->>Vercel: Trigger frontend build
1013 |     Vercel->>Vercel: Build Next.js app
1014 |     Vercel->>Vercel: Deploy to CDN
1015 |     Vercel-->>Dev: Deployment complete
1016 | ```
1017 | 
1018 | ---
1019 | 
1020 | ## 6. Development Roadmap
1021 | 
1022 | ### Phase 1: Foundation (Week 1)
1023 | - [ ] Setup Django project structure
1024 | - [ ] Configure Django Ninja API
1025 | - [ ] Implement authentication system (JWT)
1026 | - [ ] Create core models (User, Organization)
1027 | - [ ] Setup CORS configuration
1028 | - [ ] Deploy to Railway/Render
1029 | 
1030 | ### Phase 2: Core Features (Week 2)
1031 | - [ ] Implement Grant model and endpoints
1032 | - [ ] Implement Proposal model and endpoints
1033 | - [ ] Create dashboard statistics endpoints
1034 | - [ ] Setup PostgreSQL database
1035 | - [ ] Connect frontend to backend
1036 | 
1037 | ### Phase 3: AI Integration (Week 3)
1038 | - [ ] Integrate watsonx.ai provider
1039 | - [ ] Implement grant matching service
1040 | - [ ] Setup vector store (ChromaDB)
1041 | - [ ] Create proposal generation service
1042 | - [ ] Implement text improvement endpoints
1043 | 
1044 | ### Phase 4: Polish & Testing (Week 4)
1045 | - [ ] Add comprehensive error handling
1046 | - [ ] Implement rate limiting
1047 | - [ ] Setup Celery for background tasks
1048 | - [ ] Add API documentation
1049 | - [ ] Performance optimization
1050 | - [ ] Security audit
1051 | 
1052 | ---
1053 | 
1054 | ## 7. Mock Data Replacement Strategy
1055 | 
1056 | ### 7.1 Frontend Mock Data Identified
1057 | 
1058 | Based on analysis, the following mock data needs backend endpoints:
1059 | 
1060 | 1. **Dashboard Stats** (`mockStats`)
1061 |    - Active applications count
1062 |    - Total funding sought
1063 |    - Match rate percentage
1064 |    - Proposals drafted count
1065 |    - Trends data
1066 | 
1067 | 2. **Grants List** (`mockGrants`)
1068 |    - Grant details with match scores
1069 |    - Filtering and search
1070 |    - Pagination
1071 | 
1072 | 3. **Applications** (`mockApplications`)
1073 |    - Application status tracking
1074 |    - Progress indicators
1075 |    - Submission dates
1076 | 
1077 | 4. **Notifications** (`mockNotifications`)
1078 |    - Real-time notifications
1079 |    - Read/unread status
1080 |    - Notification types
1081 | 
1082 | 5. **Analytics Data**
1083 |    - Application trends over time
1084 |    - Grant category distribution
1085 |    - Success rates by category
1086 |    - Funding amount trends
1087 | 
1088 | 6. **Organization Profile** (in profile page)
1089 |    - Organization details
1090 |    - Contact information
1091 |    - Mission and goals
1092 | 
1093 | ### 7.2 API Endpoints to Replace Mock Data
1094 | 
1095 | | Frontend Mock Data | Backend Endpoint | Priority |
1096 | |-------------------|------------------|----------|
1097 | | `mockStats` | `GET /dashboard/stats` | High |
1098 | | `mockGrants` | `GET /grants?page=1&limit=20` | High |
1099 | | `mockApplications` | `GET /applications` | High |
1100 | | `mockNotifications` | `GET /dashboard/notifications` | Medium |
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
documentation\BACKEND_ARCHITECTURE_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/BACKEND_ARCHITECTURE_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:46:56.698Z
User time zone: Europe/Madrid, UTC+2:00

# Current Cost
$0.32

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<read_file>
<args>
  <file>
    <path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
    <line_range>1100-1191</line_range>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'documentation/BACKEND_ARCHITECTURE_PLAN.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
<content lines="1100-1191">
1100 | | `mockNotifications` | `GET /dashboard/notifications` | Medium |
1101 | | `applicationTrendData` | `GET /analytics/trends` | Medium |
1102 | | `grantCategoryData` | `GET /analytics/categories` | Medium |
1103 | | `successRateData` | `GET /analytics/success-rate` | Medium |
1104 | | `fundingAmountData` | `GET /analytics/funding` | Medium |
1105 | | Organization profile | `GET /organizations/{id}` | High |
1106 | | User data | `GET /auth/me` | High |
1107 | 
1108 | ---
1109 | 
1110 | ## 8. Security Checklist
1111 | 
1112 | - [x] JWT authentication with short-lived tokens
1113 | - [x] HTTPS-only in production
1114 | - [x] CORS whitelist configuration
1115 | - [x] Rate limiting on sensitive endpoints
1116 | - [x] SQL injection protection (Django ORM)
1117 | - [x] XSS protection headers
1118 | - [x] CSRF protection for state-changing operations
1119 | - [x] Password hashing (PBKDF2/Argon2)
1120 | - [x] Environment variable management
1121 | - [x] API key protection
1122 | - [x] Input validation and sanitization
1123 | - [x] Token blacklisting for logout
1124 | 
1125 | ---
1126 | 
1127 | ## 9. Next Steps
1128 | 
1129 | 1. **Review this plan** with the team
1130 | 2. **Set up development environment** with Django + Django Ninja
1131 | 3. **Create initial models** and migrations
1132 | 4. **Implement authentication** endpoints first
1133 | 5. **Deploy to Railway/Render** for testing
1134 | 6. **Connect frontend** to backend API
1135 | 7. **Iterate and refine** based on feedback
1136 | 
1137 | ---
1138 | 
1139 | ## Appendix: Quick Reference
1140 | 
1141 | ### Essential Commands
1142 | 
1143 | ```bash
1144 | # Create Django project
1145 | django-admin startproject config .
1146 | 
1147 | # Create apps
1148 | python manage.py startapp authentication
1149 | python manage.py startapp organizations
1150 | python manage.py startapp grants
1151 | python manage.py startapp proposals
1152 | python manage.py startapp ai
1153 | 
1154 | # Run migrations
1155 | python manage.py makemigrations
1156 | python manage.py migrate
1157 | 
1158 | # Create superuser
1159 | python manage.py createsuperuser
1160 | 
1161 | # Run development server
1162 | python manage.py runserver
1163 | 
1164 | # Collect static files
1165 | python manage.py collectstatic
1166 | 
1167 | # Run tests
1168 | python manage.py test
1169 | ```
1170 | 
1171 | ### Key Dependencies
1172 | 
1173 | ```txt
1174 | Django==4.2.7
1175 | django-ninja==1.0.1
1176 | django-ninja-jwt==5.2.8
1177 | django-cors-headers==4.3.1
1178 | psycopg2-binary==2.9.9
1179 | gunicorn==21.2.0
1180 | celery==5.3.4
1181 | redis==5.0.1
1182 | chromadb==0.4.18
1183 | ibm-watson-machine-learning==1.0.335
1184 | python-dotenv==1.0.0
1185 | ```
1186 | 
1187 | ---
1188 | 
1189 | **Document Version:** 1.0  
1190 | **Last Updated:** 2024-02-15  
1191 | **Author:** Backend Architecture Team
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
documentation\BACKEND_ARCHITECTURE_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/BACKEND_ARCHITECTURE_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:46:59.744Z
User time zone: Europe/Madrid, UTC+2:00

# Current Cost
$0.40

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

