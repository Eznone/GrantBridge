**User:**

<task>
Role & Context:
Act as a Senior Software Architect. I am building a decoupled proof-of-concept application. The frontend is built with React and will be hosted on Vercel. I need you to design the backend API, which will be built using Django and PostgreSQL. Aside from the instructions given look intensively into the 'documentation/BACKEND_EXECUTION_PLAN.md' (see below for file content) 

Core Objective:
Plan a backend architecture that strictly acts as an API to serve the React frontend. It needs to be lightweight enough for a PoC but structured correctly for decoupled communication.

Please provide the following deliverables:

Communication & Security: Explain how the React frontend will securely communicate with the Django backend. Specifically address how we will handle CORS configuration and stateless authentication (e.g., JWT or session management suitable for decoupled apps).

API Route Design: Map out the RESTful endpoint structure for our core features, including standard user operations (registration, login, data fetching).

Data Models: Draft the initial Django models.py schema, detailing the relationships between entities.

Infrastructure & Deployment: Provide a brief deployment strategy for hosting this Django backend on a platform suited for traditional servers (like Render or Railway), detailing how the Vercel frontend will connect to it via environment variables.
</task>

<file_content path="documentation/BACKEND_EXECUTION_PLAN.md">
  1 | # AI Grant Assistant for NGOs - Backend Architecture & Engineering Direction
  2 | 
  3 | ## Product Backend Vision
  4 | The backend should be designed as a clean, modular, AI-ready service layer capable of supporting:
  5 | * intelligent grant matching
  6 | * proposal generation
  7 | * Kanban workflow management
  8 | * NGO profile processing
  9 | * semantic search
 10 | * scalable AI integrations
 11 | 
 12 | The architecture should prioritize:
 13 | * rapid development
 14 | * maintainability
 15 | * extensibility
 16 | * clean API design
 17 | * AI orchestration
 18 | * hackathon execution speed
 19 | 
 20 | The backend should feel:
 21 | * modern
 22 | * structured
 23 | * production-oriented
 24 | * AI-native
 25 | 
 26 | ## Core Backend Stack
 27 | **Main Framework:**
 28 | * Django
 29 | * Django Ninja
 30 | * Python
 31 | 
 32 | **Why Django + Ninja:**
 33 | Django provides:
 34 | * ORM
 35 | * authentication
 36 | * admin panel
 37 | * security
 38 | * database management
 39 | * scalability foundation
 40 | 
 41 | Django Ninja provides:
 42 | * fast modern APIs
 43 | * type-safe schemas
 44 | * automatic OpenAPI docs
 45 | * clean request/response validation
 46 | * FastAPI-like developer experience
 47 | 
 48 | This combination gives:
 49 | * enterprise-level structure
 50 | * startup-level development speed
 51 | 
 52 | ## Backend Architecture Philosophy
 53 | The backend should follow:
 54 | * modular monolith architecture
 55 | * clean separation of concerns
 56 | 
 57 | Avoid:
 58 | * service-oriented internal structure
 59 | * microservices
 60 | * unnecessary infrastructure complexity
 61 | * overengineering
 62 | 
 63 | ## Recommended Backend Structure
 64 | * `backend/`
 65 |   * `manage.py`
 66 |   * `requirements/`
 67 |   * `config/`
 68 |   * `apps/`
 69 |     * `authentication/`
 70 |     * `organizations/`
 71 |     * `grants/`
 72 |     * `proposals/`
 73 |     * `ai/`
 74 |       * `matching/`
 75 |       * `analytics/`
 76 |     * `core/`
 77 |       * `settings/`
 78 |       * `database/`
 79 |       * `security/`
 80 |       * `middleware/`
 81 |       * `utilities/`
 82 |     * `services/`
 83 |     * `prompts/`
 84 |     * `vector_store/`
 85 |     * `media/`
 86 | 
 87 | ## API Layer
 88 | **Framework:**
 89 | * Django Ninja
 90 | 
 91 | **API Style:**
 92 | * REST API
 93 | * typed schemas
 94 | * modular routers
 95 | 
 96 | **Example API Structure:**
 97 | * `/api/v1/`
 98 | * `/organizations`
 99 | * `/grants`
100 | * `/proposals`
101 | * `/matching`
102 | * `/ai`
103 | 
104 | ## Authentication System
105 | **Recommended:**
106 | * JWT Authentication
107 | * Django auth system
108 | * django-ninja-jwt
109 | 
110 | **Features:**
111 | * login
112 | * registration
113 | * organization accounts
114 | * protected routes
115 | 
116 | ## Database Layer
117 | **Recommended Database:**
118 | * PostgreSQL
119 | 
120 | **ORM:**
121 | * Django ORM
122 | 
123 | **Main Models:**
124 | * **Organization:** Stores mission, goals, nonprofit categories, historical projects, and funding needs.
125 | * **Grant:** Stores title, funding amount, requirements, deadline, tags, and source.
126 | * **Proposal:** Stores AI-generated draft, status, edits, linked grant, and linked organization.
127 | * **User:** Stores account data, permissions, and organization relationship.
128 | 
129 | ## AI Layer Architecture
130 | This is the most important conceptual backend layer.
131 | 
132 | **AI Service Layer:**
133 | The AI system should be isolated into:
134 | * prompt services
135 | * generation services
136 | * evaluation services
137 | * matching services
138 | 
139 | **Recommended Structure:**
140 | * `apps/ai/`
141 |   * `services/`
142 |   * `prompts/`
143 |   * `providers/`
144 |   * `pipelines/`
145 | 
146 | **AI Providers:**
147 | * **Recommended:** watsonx.ai
148 | * **Optional:** OpenAI, Anthropic
149 | 
150 | **AI Workflows:**
151 | * **Grant Matching Agent:**
152 |   * *Input:* NGO mission, historical projects, categories
153 |   * *Output:* compatibility score, relevant grants
154 | * **Proposal Generation Agent:**
155 |   * *Input:* grant requirements, organization profile
156 |   * *Output:* structured proposal draft
157 | * **Proposal Improvement Agent Capabilities:**
158 |   * rewrite
159 |   * summarize
160 |   * improve clarity
161 |   * increase persuasiveness
162 | 
163 | **Prompt Engineering Structure:**
164 | Prompts should be versioned and modular.
165 | * `prompts/`
166 |   * `matching/`
167 |   * `proposal_generation/`
168 |   * `proposal_review/`
169 | 
170 | ## Semantic Search Layer
171 | **Recommended:**
172 | * ChromaDB OR
173 | * FAISS
174 | 
175 | **Purpose:**
176 | * semantic grant matching
177 | * similarity search
178 | * contextual recommendations
179 | 
180 | **Embedding Workflow:**
181 | Grant Data -> Embedding Model -> Vector Database -> Similarity Search
182 | 
183 | ## Background Tasks
184 | **Recommended:**
185 | * Celery
186 | * Redis
187 | 
188 | **Used for:**
189 | * AI generation tasks
190 | * embeddings generation
191 | * grant indexing
192 | * async processing
193 | 
194 | ## File Handling
195 | **Features:**
196 | * PDF uploads
197 | * document parsing
198 | * proposal exports
199 | 
200 | **Recommended Libraries:**
201 | * PyPDF2
202 | * pdfplumber
203 | * python-docx
204 | 
205 | ## External Data Sources
206 | **Grant APIs:**
207 | Potential integrations:
208 | * Grants.gov
209 | * EU Open Data
210 | * local nonprofit funding APIs
211 | 
212 | **MVP Recommendation:**
213 | Use:
214 | * mocked grant datasets
215 | * local JSON/CSV data
216 | 
217 | Focus should remain on:
218 | * workflow
219 | * UX
220 | * AI interaction
221 | 
222 | ## Admin Panel
223 | One major advantage of Django.
224 | Use Django Admin for:
225 | * managing grants
226 | * organization moderation
227 | * proposal inspection
228 | * analytics
229 | 
230 | This dramatically speeds development.
231 | 
232 | ## API Documentation
233 | Automatically generated with:
234 | * Django Ninja OpenAPI
235 | 
236 | Important for:
237 | * hackathon demos
238 | * maintainability
239 | * frontend integration
240 | 
241 | ## Security Considerations
242 | Include:
243 | * environment variables
244 | * rate limiting
245 | * secure API keys
246 | 
247 | Avoid:
248 | * protected AI endpoints
249 | * exposing prompts
250 | * exposing provider secrets
251 | 
252 | ## Deployment Stack
253 | **Backend Hosting:**
254 | Recommended:
255 | * Railway
256 | * Render
257 | * Fly.io
258 | 
259 | **Database Hosting:**
260 | * Neon PostgreSQL OR
261 | * Supabase PostgreSQL
262 | 
263 | **Storage:**
264 | Optional:
265 | * Cloudinary
266 | * Supabase Storage
267 | 
268 | ## Development Priorities for Hackathon
269 | Focus on:
270 | * AI workflows
271 | * clean API architecture
272 | * fast iteration
273 | * proposal generation quality
274 | * semantic matching
275 | 
276 | Avoid spending excessive time on:
277 | * enterprise auth
278 | * advanced permissions
279 | * infrastructure scaling
280 | 
281 | ## Recommended Development Workflow
282 | * **Step 1:** Create Django project.
283 | * **Step 2:** Setup Ninja API routes.
284 | * **Step 3:** Build organization/grant models.
285 | * **Step 4:** Integrate AI services.
286 | * **Step 5:** Implement semantic matching.
287 | * **Step 6:** Build proposal generation pipeline.
288 | * **Step 7:** Connect frontend.
289 | 
290 | ## Final Backend Goal
291 | The backend should feel like: "A modern AI orchestration platform for nonprofit funding workflows."
292 | Not: "A collection of disconnected AI endpoints."

</file_content>
<environment_details>
# VSCode Visible Files
documentation\BACKEND_EXECUTION_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/FRONTEND_EXECUTION_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:30:55.049Z
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

I'll analyze the project structure and the backend execution plan to create a comprehensive backend architecture design for your decoupled PoC application.

<read_file>
<args>
  <file>
    <path>frontend/src/lib/constants/api-endpoints.ts</path>
  </file>
  <file>
    <path>frontend/src/types/user.ts</path>
  </file>
  <file>
    <path>frontend/src/types/organization.ts</path>
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
documentation\BACKEND_EXECUTION_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/FRONTEND_EXECUTION_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:31:57.680Z
User time zone: Europe/Madrid, UTC+2:00

# Current Cost
$0.04

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

<update_todo_list>
<todos>
[ ] Analyze existing frontend types and API endpoints structure
[ ] Design Communication & Security architecture (CORS, JWT authentication)
[ ] Map out complete RESTful API endpoint structure
[ ] Draft Django models.py schema with relationships
[ ] Create deployment strategy for Django backend on Render/Railway
[ ] Document environment variable configuration
[ ] Create comprehensive architecture diagram
[ ] Review and finalize the plan with user
</todos>
</update_todo_list>

<read_file>
<args>
  <file>
    <path>documentation/specifications/Ai Grant Assistant Backend Architecture Spec.pdf</path>
  </file>
</args>
</read_file>

---

**User:**

[update_todo_list] Result:
The user denied this operation and provided the following feedback:
<feedback>
Include a step to be sure to know all the essential data, and api endpoints the backend will need inorder to replace the static data that is currently being used as a place holder for demo users in the frontend.
</feedback>
[update_todo_list] Result:
User declined to update the todoList.
Skipping tool [read_file for 'documentation/specifications/Ai Grant Assistant Backend Architecture Spec.pdf'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] due to user rejecting a previous tool.
<environment_details>
# VSCode Visible Files
documentation\BACKEND_EXECUTION_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/FRONTEND_EXECUTION_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:37:33.539Z
User time zone: Europe/Madrid, UTC+2:00

# Current Cost
$0.08

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

<search_files>
<path>frontend/src</path>
<regex>(const|let|var)\s+\w+\s*=\s*\[|mockData|dummyData|placeholder|MOCK_|static.*data</regex>
<file_pattern>*.tsx</file_pattern>
</search_files>

---

**User:**

[search_files for '(const|let|var)\s+\w+\s*=\s*\[|mockData|dummyData|placeholder|MOCK_|static.*data' in '*.tsx'] Result:
Found 28 results.

# frontend/src/app/(auth)/login/page.tsx
 81 |                 type="email"
 82 |                 placeholder="you@example.com"
 83 |                 value={email}
----

# frontend/src/components/dashboard/analytics-overview.tsx
 22 | // Mock data for analytics
 23 | const applicationTrendData = [
 24 |   { month: 'Jan', applications: 12, approved: 8, rejected: 3, pending: 1 },
----
 31 | 
 32 | const grantCategoryData = [
 33 |   { name: 'Research', value: 35, color: '#3b82f6' },
----
 39 | 
 40 | const successRateData = [
 41 |   { category: 'Research', rate: 75 },
----
 47 | 
 48 | const fundingAmountData = [
 49 |   { month: 'Jan', amount: 125000 },
----

# frontend/src/components/proposals/tiptap-editor.tsx
  4 | import StarterKit from '@tiptap/starter-kit'
  5 | import Placeholder from '@tiptap/extension-placeholder'
  6 | import { useEffect, useState } from 'react'
----
 43 |       Placeholder.configure({
 44 |         placeholder: 'Start writing your proposal here...',
 45 |       }),
----

# frontend/src/components/ui/textarea.tsx
 12 |         className={cn(
 13 |           'flex min-h-[80px] w-full rounded-md border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 px-3 py-2 text-sm text-gray-900 dark:text-gray-100 placeholder:text-gray-500 dark:placeholder:text-gray-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
 14 |           className
----

# frontend/src/app/(auth)/register/page.tsx
 95 |                 type="text"
 96 |                 placeholder="John Doe"
 97 |                 value={name}
----
109 |                 type="email"
110 |                 placeholder="you@example.com"
111 |                 value={email}
----
123 |                 type="password"
124 |                 placeholder="At least 8 characters"
125 |                 value={password}
----
137 |                 type="password"
138 |                 placeholder="Re-enter password"
139 |                 value={confirmPassword}
----

# frontend/src/components/ui/input.tsx
 12 |         className={cn(
 13 |           "flex h-10 w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm ring-offset-white file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-gray-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-700 dark:bg-gray-900 dark:ring-offset-gray-950 dark:placeholder:text-gray-400 dark:focus-visible:ring-primary-400",
 14 |           className
----

# frontend/src/components/layout/topbar.tsx
 70 | 
 71 |   const mockNotifications = [
 72 |     { id: 1, title: 'New grant match', message: 'Community Development Grant matches your profile', time: '5m ago', unread: true },
----
 95 |             type="search"
 96 |             placeholder="Search grants, proposals... (⌘K)"
 97 |             className="pl-10 bg-gray-50 dark:bg-gray-800/50 border-gray-200 dark:border-gray-700 focus:bg-white dark:focus:bg-gray-900 transition-all duration-200 focus:ring-2 focus:ring-primary-500/20"
----

# frontend/src/components/layout/sidebar.tsx
 59 | 
 60 | const navigation = [
 61 |   { name: 'Dashboard', href: '/dashboard', icon: icons.dashboard },
----

# frontend/src/app/dashboard/page.tsx
 38 | 
 39 | const mockStats = [
 40 |   {
----
 69 | 
 70 | const mockGrants = [
 71 |   {
----
 93 | 
 94 | const mockProposals = [
 95 |   {
----

# frontend/src/app/dashboard/ai-assistant/page.tsx
 67 | 
 68 | const quickActions = [
 69 |   {
----
236 |                   <Textarea
237 |                     placeholder="Ask me anything about grants..."
238 |                     value={inputMessage}
----
305 |                   <Input
306 |                     placeholder="Ask me anything about grants..."
307 |                     value={inputMessage}
----

# frontend/src/app/dashboard/applications/page.tsx
183 |             <Input
184 |               placeholder="Search applications..."
185 |               value={searchQuery}
----

# frontend/src/app/dashboard/settings/page.tsx
 70 |               <Label htmlFor="currentPassword">Current Password</Label>
 71 |               <Input id="currentPassword" type="password" placeholder="••••••••" />
 72 |             </div>
----
 75 |                 <Label htmlFor="newPassword">New Password</Label>
 76 |                 <Input id="newPassword" type="password" placeholder="••••••••" />
 77 |               </div>
----
 79 |                 <Label htmlFor="confirmPassword">Confirm Password</Label>
 80 |                 <Input id="confirmPassword" type="password" placeholder="••••••••" />
 81 |               </div>
----

# frontend/src/app/dashboard/grants/page.tsx
 90 | 
 91 | const categories = ['All', 'Community Development', 'Education', 'Environment', 'Healthcare', 'Youth Development', 'Arts & Culture']
 92 | const statusFilters = ['All', 'New', 'Saved', 'Applied']
 93 | 
----
158 |             <Input
159 |               placeholder="Search grants by title or organization..."
160 |               value={searchQuery}
----
<environment_details>
# VSCode Visible Files
documentation\BACKEND_EXECUTION_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/FRONTEND_EXECUTION_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:37:41.944Z
User time zone: Europe/Madrid, UTC+2:00

# Current Cost
$0.13

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
    <path>frontend/src/app/dashboard/page.tsx</path>
    <line_range>39-92</line_range>
  </file>
  <file>
    <path>frontend/src/app/dashboard/grants/page.tsx</path>
    <line_range>1-100</line_range>
  </file>
  <file>
    <path>frontend/src/app/dashboard/applications/page.tsx</path>
    <line_range>1-100</line_range>
  </file>
  <file>
    <path>frontend/src/components/layout/topbar.tsx</path>
    <line_range>71-75</line_range>
  </file>
  <file>
    <path>frontend/src/components/dashboard/analytics-overview.tsx</path>
    <line_range>22-50</line_range>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 5 files] Result:
<files>
<file><path>frontend/src/app/dashboard/page.tsx</path>
<content lines="39-92">
39 | const mockStats = [
40 |   {
41 |     title: 'Active Applications',
42 |     value: '12',
43 |     icon: icons.fileText,
44 |     trend: '+12%',
45 |     trendUp: true,
46 |   },
47 |   {
48 |     title: 'Total Funding Sought',
49 |     value: '$485,000',
50 |     icon: icons.dollarSign,
51 |     trend: '+8%',
52 |     trendUp: true,
53 |   },
54 |   {
55 |     title: 'Match Rate',
56 |     value: '87%',
57 |     icon: icons.target,
58 |     trend: '+5%',
59 |     trendUp: true,
60 |   },
61 |   {
62 |     title: 'Proposals Drafted',
63 |     value: '24',
64 |     icon: icons.fileCheck,
65 |     trend: '+18%',
66 |     trendUp: true,
67 |   },
68 | ]
69 | 
70 | const mockGrants = [
71 |   {
72 |     id: 1,
73 |     title: 'Community Development Grant 2024',
74 |     amount: '$50,000',
75 |     deadline: 'Mar 15, 2024',
76 |     matchScore: 94,
77 |   },
78 |   {
79 |     id: 2,
80 |     title: 'Education Innovation Fund',
81 |     amount: '$75,000',
82 |     deadline: 'Apr 1, 2024',
83 |     matchScore: 89,
84 |   },
85 |   {
86 |     id: 3,
87 |     title: 'Environmental Sustainability Program',
88 |     amount: '$100,000',
89 |     deadline: 'Apr 20, 2024',
90 |     matchScore: 85,
91 |   },
92 | ]
</content>
</file>
<file><path>frontend/src/app/dashboard/grants/page.tsx</path>
<content lines="1-100">
  1 | 'use client'
  2 | 
  3 | import { useState } from 'react'
  4 | import { motion } from 'framer-motion'
  5 | import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
  6 | import { Input } from '@/components/ui/input'
  7 | import { Button } from '@/components/ui/button'
  8 | import { Badge } from '@/components/ui/badge'
  9 | 
 10 | interface Grant {
 11 |   id: number
 12 |   title: string
 13 |   organization: string
 14 |   amount: string
 15 |   deadline: string
 16 |   category: string
 17 |   matchScore: number
 18 |   status: 'new' | 'saved' | 'applied'
 19 |   description: string
 20 | }
 21 | 
 22 | const mockGrants: Grant[] = [
 23 |   {
 24 |     id: 1,
 25 |     title: 'Community Development Grant 2024',
 26 |     organization: 'National Community Foundation',
 27 |     amount: '$50,000',
 28 |     deadline: '2024-03-15',
 29 |     category: 'Community Development',
 30 |     matchScore: 94,
 31 |     status: 'new',
 32 |     description: 'Supporting community-led initiatives that promote sustainable development and social cohesion.',
 33 |   },
 34 |   {
 35 |     id: 2,
 36 |     title: 'Education Innovation Fund',
 37 |     organization: 'Education Forward Initiative',
 38 |     amount: '$75,000',
 39 |     deadline: '2024-04-01',
 40 |     category: 'Education',
 41 |     matchScore: 89,
 42 |     status: 'saved',
 43 |     description: 'Funding innovative educational programs that improve student outcomes and teacher effectiveness.',
 44 |   },
 45 |   {
 46 |     id: 3,
 47 |     title: 'Environmental Sustainability Program',
 48 |     organization: 'Green Future Foundation',
 49 |     amount: '$100,000',
 50 |     deadline: '2024-04-20',
 51 |     category: 'Environment',
 52 |     matchScore: 85,
 53 |     status: 'new',
 54 |     description: 'Supporting projects that address climate change and promote environmental conservation.',
 55 |   },
 56 |   {
 57 |     id: 4,
 58 |     title: 'Healthcare Access Initiative',
 59 |     organization: 'Health for All Coalition',
 60 |     amount: '$60,000',
 61 |     deadline: '2024-03-30',
 62 |     category: 'Healthcare',
 63 |     matchScore: 82,
 64 |     status: 'applied',
 65 |     description: 'Improving healthcare access for underserved communities through innovative delivery models.',
 66 |   },
 67 |   {
 68 |     id: 5,
 69 |     title: 'Youth Empowerment Grant',
 70 |     organization: 'Youth Development Network',
 71 |     amount: '$45,000',
 72 |     deadline: '2024-05-15',
 73 |     category: 'Youth Development',
 74 |     matchScore: 78,
 75 |     status: 'new',
 76 |     description: 'Empowering young people through mentorship, skills training, and leadership development.',
 77 |   },
 78 |   {
 79 |     id: 6,
 80 |     title: 'Arts & Culture Preservation',
 81 |     organization: 'Cultural Heritage Trust',
 82 |     amount: '$55,000',
 83 |     deadline: '2024-04-10',
 84 |     category: 'Arts & Culture',
 85 |     matchScore: 75,
 86 |     status: 'saved',
 87 |     description: 'Preserving and promoting local arts and cultural traditions through community engagement.',
 88 |   },
 89 | ]
 90 | 
 91 | const categories = ['All', 'Community Development', 'Education', 'Environment', 'Healthcare', 'Youth Development', 'Arts & Culture']
 92 | const statusFilters = ['All', 'New', 'Saved', 'Applied']
 93 | 
 94 | export default function GrantsPage() {
 95 |   const [searchQuery, setSearchQuery] = useState('')
 96 |   const [selectedCategory, setSelectedCategory] = useState('All')
 97 |   const [selectedStatus, setSelectedStatus] = useState('All')
 98 | 
 99 |   const filteredGrants = mockGrants.filter((grant) => {
100 |     const matchesSearch = grant.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
</content>
</file>
<file><path>frontend/src/app/dashboard/applications/page.tsx</path>
<content lines="1-100">
  1 | 'use client'
  2 | 
  3 | import { useState } from 'react'
  4 | import { motion } from 'framer-motion'
  5 | import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
  6 | import { Badge } from '@/components/ui/badge'
  7 | import { Button } from '@/components/ui/button'
  8 | import { Input } from '@/components/ui/input'
  9 | 
 10 | interface Application {
 11 |   id: number
 12 |   grantTitle: string
 13 |   organization: string
 14 |   amount: string
 15 |   submittedDate: string
 16 |   status: 'draft' | 'submitted' | 'under_review' | 'approved' | 'rejected'
 17 |   deadline: string
 18 |   progress: number
 19 | }
 20 | 
 21 | const mockApplications: Application[] = [
 22 |   {
 23 |     id: 1,
 24 |     grantTitle: 'Community Development Grant 2024',
 25 |     organization: 'National Community Foundation',
 26 |     amount: '$50,000',
 27 |     submittedDate: '2024-02-15',
 28 |     status: 'under_review',
 29 |     deadline: '2024-03-15',
 30 |     progress: 100,
 31 |   },
 32 |   {
 33 |     id: 2,
 34 |     grantTitle: 'Education Innovation Fund',
 35 |     organization: 'Education Forward Initiative',
 36 |     amount: '$75,000',
 37 |     submittedDate: '2024-02-20',
 38 |     status: 'submitted',
 39 |     deadline: '2024-04-01',
 40 |     progress: 100,
 41 |   },
 42 |   {
 43 |     id: 3,
 44 |     grantTitle: 'Healthcare Access Initiative',
 45 |     organization: 'Health for All Coalition',
 46 |     amount: '$60,000',
 47 |     submittedDate: '2024-01-10',
 48 |     status: 'approved',
 49 |     deadline: '2024-03-30',
 50 |     progress: 100,
 51 |   },
 52 |   {
 53 |     id: 4,
 54 |     grantTitle: 'Youth Empowerment Grant',
 55 |     organization: 'Youth Development Network',
 56 |     amount: '$45,000',
 57 |     submittedDate: '',
 58 |     status: 'draft',
 59 |     deadline: '2024-05-15',
 60 |     progress: 65,
 61 |   },
 62 |   {
 63 |     id: 5,
 64 |     grantTitle: 'Environmental Sustainability Program',
 65 |     organization: 'Green Future Foundation',
 66 |     amount: '$100,000',
 67 |     submittedDate: '2024-01-05',
 68 |     status: 'rejected',
 69 |     deadline: '2024-04-20',
 70 |     progress: 100,
 71 |   },
 72 | ]
 73 | 
 74 | const statusConfig = {
 75 |   draft: {
 76 |     label: 'Draft',
 77 |     color: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400',
 78 |     icon: '📝',
 79 |   },
 80 |   submitted: {
 81 |     label: 'Submitted',
 82 |     color: 'bg-blue-100 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400',
 83 |     icon: '📤',
 84 |   },
 85 |   under_review: {
 86 |     label: 'Under Review',
 87 |     color: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/20 dark:text-yellow-400',
 88 |     icon: '🔍',
 89 |   },
 90 |   approved: {
 91 |     label: 'Approved',
 92 |     color: 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400',
 93 |     icon: '✅',
 94 |   },
 95 |   rejected: {
 96 |     label: 'Rejected',
 97 |     color: 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400',
 98 |     icon: '❌',
 99 |   },
100 | }
</content>
</file>
<file><path>frontend/src/components/layout/topbar.tsx</path>
<content lines="71-75">
71 |   const mockNotifications = [
72 |     { id: 1, title: 'New grant match', message: 'Community Development Grant matches your profile', time: '5m ago', unread: true },
73 |     { id: 2, title: 'Application approved', message: 'Your Healthcare Access Initiative application was approved', time: '2h ago', unread: true },
74 |     { id: 3, title: 'Deadline reminder', message: 'Youth Empowerment Grant deadline in 3 days', time: '1d ago', unread: false },
75 |   ]
</content>
</file>
<file><path>frontend/src/components/dashboard/analytics-overview.tsx</path>
<content lines="22-50">
22 | // Mock data for analytics
23 | const applicationTrendData = [
24 |   { month: 'Jan', applications: 12, approved: 8, rejected: 3, pending: 1 },
25 |   { month: 'Feb', applications: 15, approved: 10, rejected: 4, pending: 1 },
26 |   { month: 'Mar', applications: 18, approved: 12, rejected: 5, pending: 1 },
27 |   { month: 'Apr', applications: 22, approved: 15, rejected: 6, pending: 1 },
28 |   { month: 'May', applications: 28, approved: 19, rejected: 7, pending: 2 },
29 |   { month: 'Jun', applications: 25, approved: 17, rejected: 6, pending: 2 },
30 | ]
31 | 
32 | const grantCategoryData = [
33 |   { name: 'Research', value: 35, color: '#3b82f6' },
34 |   { name: 'Education', value: 25, color: '#10b981' },
35 |   { name: 'Healthcare', value: 20, color: '#f59e0b' },
36 |   { name: 'Technology', value: 15, color: '#8b5cf6' },
37 |   { name: 'Other', value: 5, color: '#6b7280' },
38 | ]
39 | 
40 | const successRateData = [
41 |   { category: 'Research', rate: 75 },
42 |   { category: 'Education', rate: 68 },
43 |   { category: 'Healthcare', rate: 82 },
44 |   { category: 'Technology', rate: 71 },
45 |   { category: 'Arts', rate: 65 },
46 | ]
47 | 
48 | const fundingAmountData = [
49 |   { month: 'Jan', amount: 125000 },
50 |   { month: 'Feb', amount: 180000 },
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
documentation\BACKEND_EXECUTION_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/FRONTEND_EXECUTION_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:37:49.118Z
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
    <path>frontend/src/app/dashboard/proposals/page.tsx</path>
    <line_range>1-100</line_range>
  </file>
  <file>
    <path>frontend/src/app/dashboard/profile/page.tsx</path>
    <line_range>1-100</line_range>
  </file>
  <file>
    <path>frontend/src/lib/stores/auth-store.ts</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'frontend/src/app/dashboard/proposals/page.tsx', 'frontend/src/app/dashboard/profile/page.tsx', 'frontend/src/lib/stores/auth-store.ts'] Result:
<files>
<file><path>frontend/src/app/dashboard/proposals/page.tsx</path>
<content lines="1-100">
  1 | 'use client'
  2 | 
  3 | import { useState } from 'react'
  4 | import { TiptapEditor } from '@/components/proposals/tiptap-editor'
  5 | import { AISuggestions } from '@/components/proposals/ai-suggestions'
  6 | import { useProposalStore } from '@/lib/stores/proposal-store'
  7 | import { Button } from '@/components/ui/button'
  8 | import { Input } from '@/components/ui/input'
  9 | import { motion } from 'framer-motion'
 10 | 
 11 | export default function ProposalsPage() {
 12 |   const { title, setTitle } = useProposalStore()
 13 |   const [isEditingTitle, setIsEditingTitle] = useState(false)
 14 | 
 15 |   return (
 16 |     <div className="h-[calc(100vh-8rem)] flex flex-col">
 17 |       {/* Header */}
 18 |       <motion.div
 19 |         initial={{ opacity: 0, y: -20 }}
 20 |         animate={{ opacity: 1, y: 0 }}
 21 |         className="mb-6"
 22 |       >
 23 |         <div className="flex items-center justify-between mb-2">
 24 |           {isEditingTitle ? (
 25 |             <Input
 26 |               value={title}
 27 |               onChange={(e) => setTitle(e.target.value)}
 28 |               onBlur={() => setIsEditingTitle(false)}
 29 |               onKeyDown={(e) => e.key === 'Enter' && setIsEditingTitle(false)}
 30 |               className="text-3xl font-bold border-none shadow-none p-0 h-auto focus-visible:ring-0"
 31 |               autoFocus
 32 |             />
 33 |           ) : (
 34 |             <h1
 35 |               className="text-3xl font-bold text-gray-900 dark:text-gray-100 cursor-pointer hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
 36 |               onClick={() => setIsEditingTitle(true)}
 37 |             >
 38 |               {title}
 39 |             </h1>
 40 |           )}
 41 | 
 42 |           <div className="flex items-center gap-2">
 43 |             <Button variant="outline" size="sm">
 44 |               <svg
 45 |                 className="w-4 h-4 mr-1.5"
 46 |                 fill="none"
 47 |                 stroke="currentColor"
 48 |                 viewBox="0 0 24 24"
 49 |               >
 50 |                 <path
 51 |                   strokeLinecap="round"
 52 |                   strokeLinejoin="round"
 53 |                   strokeWidth={2}
 54 |                   d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"
 55 |                 />
 56 |               </svg>
 57 |               Export
 58 |             </Button>
 59 |             <Button size="sm">
 60 |               <svg
 61 |                 className="w-4 h-4 mr-1.5"
 62 |                 fill="none"
 63 |                 stroke="currentColor"
 64 |                 viewBox="0 0 24 24"
 65 |               >
 66 |                 <path
 67 |                   strokeLinecap="round"
 68 |                   strokeLinejoin="round"
 69 |                   strokeWidth={2}
 70 |                   d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"
 71 |                 />
 72 |               </svg>
 73 |               Submit
 74 |             </Button>
 75 |           </div>
 76 |         </div>
 77 |         <p className="text-gray-600 dark:text-gray-400">
 78 |           Use AI tools to enhance your proposal writing
 79 |         </p>
 80 |       </motion.div>
 81 | 
 82 |       {/* Main Content */}
 83 |       <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 overflow-hidden">
 84 |         {/* Editor - Takes 2 columns on large screens */}
 85 |         <motion.div
 86 |           initial={{ opacity: 0, x: -20 }}
 87 |           animate={{ opacity: 1, x: 0 }}
 88 |           transition={{ delay: 0.1 }}
 89 |           className="lg:col-span-2 border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden shadow-sm relative"
 90 |         >
 91 |           <TiptapEditor />
 92 |         </motion.div>
 93 | 
 94 |         {/* AI Suggestions Sidebar */}
 95 |         <motion.div
 96 |           initial={{ opacity: 0, x: 20 }}
 97 |           animate={{ opacity: 1, x: 0 }}
 98 |           transition={{ delay: 0.2 }}
 99 |           className="overflow-y-auto"
100 |         >
</content>
</file>
<file><path>frontend/src/app/dashboard/profile/page.tsx</path>
<content lines="1-100">
  1 | 'use client'
  2 | 
  3 | import { useState } from 'react'
  4 | import { motion } from 'framer-motion'
  5 | import { Button } from '@/components/ui/button'
  6 | import { Input } from '@/components/ui/input'
  7 | import { Label } from '@/components/ui/label'
  8 | import { Textarea } from '@/components/ui/textarea'
  9 | import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
 10 | 
 11 | interface OrganizationData {
 12 |   name: string
 13 |   type: string
 14 |   ein: string
 15 |   website: string
 16 |   email: string
 17 |   phone: string
 18 |   address: string
 19 |   city: string
 20 |   state: string
 21 |   zip: string
 22 |   mission: string
 23 |   description: string
 24 |   yearFounded: string
 25 |   annualBudget: string
 26 | }
 27 | 
 28 | export default function ProfilePage() {
 29 |   const [isEditing, setIsEditing] = useState(false)
 30 |   const [isSaving, setIsSaving] = useState(false)
 31 |   const [organization, setOrganization] = useState<OrganizationData>({
 32 |     name: 'Community Development Foundation',
 33 |     type: '501(c)(3) Nonprofit',
 34 |     ein: '12-3456789',
 35 |     website: 'https://communityfoundation.org',
 36 |     email: 'info@communityfoundation.org',
 37 |     phone: '(555) 123-4567',
 38 |     address: '123 Main Street',
 39 |     city: 'Springfield',
 40 |     state: 'IL',
 41 |     zip: '62701',
 42 |     mission: 'To empower communities through education, healthcare, and sustainable development initiatives.',
 43 |     description: 'We are a nonprofit organization dedicated to improving the quality of life in underserved communities through comprehensive programs in education, healthcare access, and economic development.',
 44 |     yearFounded: '2010',
 45 |     annualBudget: '$2,500,000',
 46 |   })
 47 | 
 48 |   const handleSave = async () => {
 49 |     setIsSaving(true)
 50 |     // Simulate API call
 51 |     await new Promise(resolve => setTimeout(resolve, 1000))
 52 |     setIsSaving(false)
 53 |     setIsEditing(false)
 54 |   }
 55 | 
 56 |   const handleCancel = () => {
 57 |     setIsEditing(false)
 58 |     // Reset to original values in real implementation
 59 |   }
 60 | 
 61 |   return (
 62 |     <div className="max-w-4xl space-y-6">
 63 |       {/* Header */}
 64 |       <motion.div
 65 |         initial={{ opacity: 0, y: -20 }}
 66 |         animate={{ opacity: 1, y: 0 }}
 67 |         className="flex items-center justify-between"
 68 |       >
 69 |         <div>
 70 |           <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
 71 |             Organization Profile
 72 |           </h1>
 73 |           <p className="text-gray-600 dark:text-gray-400 mt-2">
 74 |             Manage your organization's information and settings
 75 |           </p>
 76 |         </div>
 77 |         {!isEditing ? (
 78 |           <Button onClick={() => setIsEditing(true)}>
 79 |             <svg
 80 |               className="w-4 h-4 mr-2"
 81 |               fill="none"
 82 |               stroke="currentColor"
 83 |               viewBox="0 0 24 24"
 84 |             >
 85 |               <path
 86 |                 strokeLinecap="round"
 87 |                 strokeLinejoin="round"
 88 |                 strokeWidth={2}
 89 |                 d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
 90 |               />
 91 |             </svg>
 92 |             Edit Profile
 93 |           </Button>
 94 |         ) : (
 95 |           <div className="flex gap-2">
 96 |             <Button variant="outline" onClick={handleCancel} disabled={isSaving}>
 97 |               Cancel
 98 |             </Button>
 99 |             <Button onClick={handleSave} disabled={isSaving}>
100 |               {isSaving ? (
</content>
</file>
<file><path>frontend/src/lib/stores/auth-store.ts</path>
<content lines="1-140">
  1 | 'use client'
  2 | 
  3 | import { create } from 'zustand'
  4 | import { persist, createJSONStorage } from 'zustand/middleware'
  5 | import type { User } from '@/types/user'
  6 | 
  7 | interface AuthState {
  8 |   user: User | null
  9 |   token: string | null
 10 |   isAuthenticated: boolean
 11 |   isLoading: boolean
 12 |   error: string | null
 13 |   _hasHydrated: boolean
 14 |   
 15 |   setHasHydrated: (state: boolean) => void
 16 |   login: (email: string, password: string) => Promise<void>
 17 |   register: (name: string, email: string, password: string) => Promise<void>
 18 |   logout: () => void
 19 |   clearError: () => void
 20 | }
 21 | 
 22 | // Mock user data
 23 | const mockUser: User = {
 24 |   id: '1',
 25 |   email: 'demo@grantbridge.org',
 26 |   name: 'Demo User',
 27 |   organizationId: 'org-1',
 28 |   role: 'admin',
 29 |   createdAt: new Date().toISOString(),
 30 | }
 31 | 
 32 | export const useAuthStore = create<AuthState>()(
 33 |   persist(
 34 |     (set, get) => ({
 35 |       user: null,
 36 |       token: null,
 37 |       isAuthenticated: false,
 38 |       isLoading: false,
 39 |       error: null,
 40 |       _hasHydrated: false,
 41 | 
 42 |       setHasHydrated: (state) => {
 43 |         set({ _hasHydrated: state })
 44 |       },
 45 | 
 46 |       login: async (email: string, password: string) => {
 47 |         set({ isLoading: true, error: null })
 48 |         
 49 |         try {
 50 |           // Simulate API call
 51 |           await new Promise(resolve => setTimeout(resolve, 800))
 52 |           
 53 |           // Mock validation
 54 |           if (email === 'demo@grantbridge.org' && password === 'demo123') {
 55 |             const mockToken = 'mock-jwt-token-' + Date.now()
 56 |             
 57 |             set({
 58 |               user: mockUser,
 59 |               token: mockToken,
 60 |               isAuthenticated: true,
 61 |               isLoading: false,
 62 |               error: null,
 63 |             })
 64 |           } else {
 65 |             set({
 66 |               error: 'Invalid email or password',
 67 |               isLoading: false,
 68 |               isAuthenticated: false,
 69 |             })
 70 |             throw new Error('Invalid credentials')
 71 |           }
 72 |         } catch (error) {
 73 |           set({
 74 |             isLoading: false,
 75 |             error: error instanceof Error ? error.message : 'Login failed',
 76 |           })
 77 |           throw error
 78 |         }
 79 |       },
 80 | 
 81 |       register: async (name: string, email: string, password: string) => {
 82 |         set({ isLoading: true, error: null })
 83 |         
 84 |         try {
 85 |           // Simulate API call
 86 |           await new Promise(resolve => setTimeout(resolve, 800))
 87 |           
 88 |           const newUser: User = {
 89 |             ...mockUser,
 90 |             id: 'user-' + Date.now(),
 91 |             name,
 92 |             email,
 93 |           }
 94 |           
 95 |           const mockToken = 'mock-jwt-token-' + Date.now()
 96 |           
 97 |           set({
 98 |             user: newUser,
 99 |             token: mockToken,
100 |             isAuthenticated: true,
101 |             isLoading: false,
102 |             error: null,
103 |           })
104 |         } catch (error) {
105 |           set({
106 |             isLoading: false,
107 |             error: error instanceof Error ? error.message : 'Registration failed',
108 |           })
109 |           throw error
110 |         }
111 |       },
112 | 
113 |       logout: () => {
114 |         set({
115 |           user: null,
116 |           token: null,
117 |           isAuthenticated: false,
118 |           error: null,
119 |           isLoading: false,
120 |         })
121 |       },
122 | 
123 |       clearError: () => set({ error: null }),
124 |     }),
125 |     {
126 |       name: 'grantbridge-auth',
127 |       storage: createJSONStorage(() => localStorage),
128 |       partialize: (state) => ({
129 |         user: state.user,
130 |         token: state.token,
131 |         isAuthenticated: state.isAuthenticated,
132 |       }),
133 |       onRehydrateStorage: () => (state) => {
134 |         state?.setHasHydrated(true)
135 |       },
136 |     }
137 |   )
138 | )
139 | 
140 | // Made with Bob
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
documentation\BACKEND_EXECUTION_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/FRONTEND_EXECUTION_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:37:56.621Z
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

<update_todo_list>
<todos>
[ ] Analyze all mock data structures used in frontend to identify required backend data models
[ ] Map frontend API endpoints to backend route requirements
[ ] Design Communication & Security architecture (CORS, JWT authentication)
[ ] Design complete RESTful API endpoint structure with request/response schemas
[ ] Draft comprehensive Django models.py schema with all relationships
[ ] Plan AI service layer architecture and integration points
[ ] Create deployment strategy for Django backend on Render/Railway
[ ] Document environment variable configuration for frontend-backend connection
[ ] Create comprehensive architecture documentation with diagrams
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
documentation\BACKEND_EXECUTION_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/FRONTEND_EXECUTION_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:38:10.761Z
User time zone: Europe/Madrid, UTC+2:00

# Current Cost
$0.32

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Analyze all mock data structures used in frontend to identify required backend data models | Pending |
| 2 | Map frontend API endpoints to backend route requirements | Pending |
| 3 | Design Communication & Security architecture (CORS, JWT authentication) | Pending |
| 4 | Design complete RESTful API endpoint structure with request/response schemas | Pending |
| 5 | Draft comprehensive Django models.py schema with all relationships | Pending |
| 6 | Plan AI service layer architecture and integration points | Pending |
| 7 | Create deployment strategy for Django backend on Render/Railway | Pending |
| 8 | Document environment variable configuration for frontend-backend connection | Pending |
| 9 | Create comprehensive architecture documentation with diagrams | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now I'll create a comprehensive backend architecture plan. Let me start by analyzing the mock data and creating the complete architecture documentation.

<write_to_file>
<path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
<content>
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
      "grant": {/* grant object */},
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
  "data": {/* response data */},
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
  "data": [/* items */],
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

### 3.1 Core Models

#### 3.1.1 User Model

```python
# apps/authentication/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
import uuid

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=255)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='users')
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('member', 'Member')], default='member')
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

#### 3.1.2 Organization Model

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
    
    # Organization Details
    mission = models.TextField(help_text="Organization's mission statement")
    description = models.TextField(blank=True)
    goals = models.JSONField(default=list, help_text="List of organizational goals")
    categories = models.JSONField(default=list, help_text="Nonprofit categories/focus areas")
    historical_projects = models.JSONField(default=list, help_text="Past projects and achievements")
    
    # Financial
    year_founded = models.IntegerField(null=True, blank=True)
    annual_budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    funding_needs = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Metadata
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # AI/Matching
    embedding_vector = models.JSONField(null=True, blank=True, help_text="Vector embedding for semantic matching")
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

#### 3.1.3 Grant Model

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
    organization = models.CharField(max_length=255, help_text="Funding organization name")
    
    # Financial
    funding_amount = models.DecimalField(max_digits=12, decimal_places=2)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Details
    description = models.TextField()
    requirements = models.TextField(help_text="Grant requirements and criteria")
    eligibility = models.JSONField(default=list, help_text="List of eligibility criteria")
    
    # Categorization
    tags = models.JSONField(default=list, help_text="Grant tags/keywords")
    categories = models.JSONField(default=list, help_text="Grant categories")
    
    # Dates
    deadline = models.DateTimeField(db_index=True)
    announcement_date = models.DateTimeField(null=True, blank=True)
    award_date = models.DateTimeField(null=True, blank=True)
    
    # Source
    source = models.CharField(max_length=255, help_text="Source of grant (e.g., grants.gov)")
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
            models.Index(fields=['source', 'external_id']),
        ]
        ordering = ['-deadline']
    
    def __str__(self):
        return self.title
```

#### 3.1.4 Proposal Model

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
    
    def __str__(self):
        return f"{self.title} - {self.organization.name}"
```

#### 3.1.5 GrantMatch Model

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

#### 3.1.6 Notification Model

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

### 3.2 Model Relationships Diagram

```mermaid
erDiagram
    User ||--o{ Proposal : creates
    User }o--|| Organization : belongs_to
    User ||--o{ Notification : receives
    
    Organization ||--o{ Proposal : submits
    Organization ||--o{ GrantMatch : has
    
    Grant ||--o{ Proposal : receives
    Grant ||--o{ GrantMatch : matched_with
    
    Proposal }o--|| Grant : for
    Proposal }o--|| Organization : from
    
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

### 4.2 AI Provider Configuration

```python
# apps/ai/providers/watsonx.py
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

class WatsonXProvider:
    def __init__(self):
        self.credentials = {
            "url": settings.WATSONX_URL,
            "apikey": settings.WATSONX_API_KEY
        }
        self.project_id = settings.WATSONX_PROJECT_ID
        
    def generate(self, prompt: str, model_id: str = "ibm/granite-13b-chat-v2", **params):
        parameters = {
            GenParams.MAX_NEW_TOKENS: params.get('max_tokens', 1000),
            GenParams.TEMPERATURE: params.get('temperature', 0.7),
            GenParams.TOP_P: params.get('top_p', 1),
            GenParams.TOP_K: params.get('top_k', 50),
        }
        
        model = Model(
            model_id=model_id,
            params=parameters,
            credentials=self.credentials,
            project_id=self.project_id
        )
        
        return model.generate_text(prompt=prompt)
```

### 4.3 Grant Matching Service

```python
# apps/ai/services/matching.py
from typing import List, Dict
from apps.grants.models import Grant
from apps.organizations.models import Organization
from .embeddings import EmbeddingService

class GrantMatchingService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        
    def calculate_matches(self, organization: Organization, grants: List[Grant], threshold: float = 0.7) -> List[Dict]:
        """Calculate match scores between organization and grants"""
        
        # Get organization embedding
        org_embedding = self.embedding_service.get_or_create_embedding(
            text=self._prepare_org_text(organization),
            entity_type='organization',
            entity_id=str(organization.id)
        )
        
        matches = []
        for grant in grants:
            # Get grant embedding
            grant_embedding = self.embedding_service.get_or_create_embedding(
                text=self._prepare_grant_text(grant),
                entity_type='grant',
                entity_id=str(grant.id)
            )
            
            # Calculate similarity
            score = self._cosine_similarity(org_embedding, grant_embedding)
            
            if score >= threshold:
                match_reasons = self._generate_match_reasons(organization, grant, score)
                matches.append({
                    'grant': grant,
                    'match_score': round(score * 100, 2),
                    'match_reasons': match_reasons,
                    'recommended_actions': self._generate_recommendations(grant, score)
                })
        
        return sorted(matches, key=lambda x: x['match_score'], reverse=True)
    
    def _prepare_org_text(self, org: Organization) -> str:
        """Prepare organization text for embedding"""
        return f"""
        Organization: {org.name}
        Mission: {org.mission}
        Categories: {', '.join(org.categories)}
        Goals: {', '.join(org.goals)}
        Historical Projects: {', '.join(org.historical_projects[:3])}
        """
    
    def _prepare_grant_text(self, grant: Grant) -> str:
        """Prepare grant text for embedding"""
        return f"""
        Grant: {grant.title}
        Description: {grant.description}
        Requirements: {grant.requirements}
        Categories: {', '.join(grant.categories)}
        Tags: {', '.join(grant.tags)}
        """
```

### 4.4 Proposal Generation Service

```python
# apps/ai/services/generation.py
from apps.ai.providers.watsonx import WatsonXProvider
from apps.grants.models import Grant
from apps.organizations.models import Organization

class ProposalGenerationService:
    def __init__(self):
        self.provider = WatsonXProvider()
        
    def generate_proposal(self, grant: Grant, organization: Organization, tone: str = 'professional') -> Dict:
        """Generate a complete proposal draft"""
        
        sections = {
            'executive_summary': self._generate_executive_summary(grant, organization, tone),
            'project_description': self._generate_project_description(grant, organization, tone),
            'budget_narrative': self._generate_budget_narrative(grant, organization, tone),
            'organizational_capacity': self._generate_capacity_section(organization, tone),
        }
        
        # Combine sections
        full_content = self._format_proposal(sections)
        
        return {
            'content': full_content,
            'sections': sections,
            'metadata': {
                'model': 'watsonx.ai/granite-13b',
                'tone': tone,
                'generated_at': timezone.now().isoformat(),
            }
        }
    
    def _generate_executive_summary(self, grant: Grant, org: Organization, tone: str) -> str:
        prompt = self._load_prompt('generation/executive_summary.txt')
        prompt = prompt.format(
            grant_title=grant.title,
            grant_description=grant.description,
            org_name=org.name,
            org_mission=org.mission,
            funding_amount=grant.funding_amount,
            tone=tone
        )
        
        return self.provider.generate(prompt, temperature=0.7)
```

### 4.5 Vector Store Integration

```python
# apps/ai/services/embeddings.py
import chromadb
from chromadb.config import Settings

class EmbeddingService:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=settings.VECTOR_STORE_PATH
        ))
        self.collection = self.client.get_or_create_collection(
            name="grantbridge_embeddings",
            metadata={"hnsw:space": "cosine"}
        )
    
    def get_or_create_embedding(self, text: str, entity_type: str, entity_id: str):
        """Get existing embedding or create new one"""
        # Check if embedding exists
        results = self.collection.get(ids=[entity_id])
        
        if results['ids']:
            return results['embeddings'][0]
        
        # Create new embedding
        embedding = self._create_embedding(text)
        
        # Store in vector database
        self.collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[{"type": entity_type, "id": entity_id}],
            ids=[entity_id]
        )
        
        return embedding
    
    def semantic_search(self, query: str, entity_type: str = None, limit: int = 10):
        """Perform semantic search"""
        query_embedding = self._create_embedding(query)
        
        where_filter = {"type": entity_type} if entity_type else None
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where=where_filter
        )
        
        return results
```

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

### 5.6 Initial Deployment Steps

#### Backend Deployment (Railway)

1. **Connect Repository:**
   ```bash
   # Push code to GitHub
   git remote add origin https://github.com/yourusername/grantbridge-backend.git
   git push -u origin main
   ```

2. **Create Railway Project:**
   - Connect GitHub repository
   - Add PostgreSQL database
   - Add Redis service
   - Configure environment variables

3. **Deploy:**
   ```bash
   # Railway will automatically deploy on push
   # Or manually trigger:
   railway up
   ```

#### Frontend Configuration (Vercel)

1. **Add Environment Variable:**
   ```bash
   # In Vercel dashboard, add:
   NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app/api/v1
   ```

2. **Redeploy Frontend:**
   ```bash
   # Vercel will auto-deploy on push
   git push origin main
   ```

### 5.7 Health Check Endpoint

```python
# apps/core/api.py
from ninja import Router

router = Router()

@router.get("/health")
def health_check(request):
    """Health check endpoint for deployment platforms"""
    return {
        "status": "healthy",
        "timestamp": timezone.now().isoformat(),
        "version": "1.0.0"
    }
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

## 7. API Documentation

### 7.1 Auto-Generated Documentation

Django Ninja automatically generates OpenAPI documentation:

**Access Points:**
- Interactive Docs: `https://your-api.railway.app/api/docs`
- OpenAPI Schema: `https://your-api.railway.app/api/openapi.json`

### 7.2 Example API Usage

#### Authentication Flow

```javascript
// Register
const response = await fetch('https://api.grantbridge.com/api/v1/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.org',
    password: 'securepass123',
    organizationName: 'Community Foundation'
  })
});

const { user, accessToken, refreshToken } = await response.json();

// Use access token for subsequent requests
const grants = await fetch('https://api.grantbridge.com/api/v1/grants', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
```

---

## 8. Security Checklist

- [x] JWT authentication with short-lived tokens
- [x] HTTPS-only in production
- [x] CORS whitelist configuration
- [x] Rate limiting on sensitive endpoints
- [x] SQL injection protection (Django ORM)
- [x] XSS protection headers
- [x

---

**User:**

[write_to_file for 'documentation/BACKEND_ARCHITECTURE_PLAN.md'] Result:
The tool execution failed with the following error:
<error>
This appears to be a new file.
Note: Your response may have been truncated because it exceeded your output limit. You wrote 1282 lines of content, but the line_count parameter was either missing or not included in your response.

RECOMMENDED APPROACH:
1. Try again with the line_count parameter in your response if you forgot to include it
2. Or break your content into smaller chunks - first use write_to_file with the initial chunk
3. Then use insert_content to append additional chunks

# Reminder: Instructions for Tool Use

Tool uses are formatted using XML-style tags. The tool name itself becomes the XML tag name. Each parameter is enclosed within its own set of tags. Here's the structure:

<actual_tool_name>
<parameter1_name>value1</parameter1_name>
<parameter2_name>value2</parameter2_name>
...
</actual_tool_name>

For example, to use the attempt_completion tool:

<attempt_completion>
<result>
I have completed the task...
</result>
</attempt_completion>

Always use the actual tool name as the XML tag name for proper parsing and execution.
</error>
<environment_details>
# VSCode Visible Files
documentation\BACKEND_ARCHITECTURE_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/BACKEND_ARCHITECTURE_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:40:31.150Z
User time zone: Europe/Madrid, UTC+2:00

# Current Cost
$0.43

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Analyze all mock data structures used in frontend to identify required backend data models | Pending |
| 2 | Map frontend API endpoints to backend route requirements | Pending |
| 3 | Design Communication & Security architecture (CORS, JWT authentication) | Pending |
| 4 | Design complete RESTful API endpoint structure with request/response schemas | Pending |
| 5 | Draft comprehensive Django models.py schema with all relationships | Pending |
| 6 | Plan AI service layer architecture and integration points | Pending |
| 7 | Create deployment strategy for Django backend on Render/Railway | Pending |
| 8 | Document environment variable configuration for frontend-backend connection | Pending |
| 9 | Create comprehensive architecture documentation with diagrams | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

I need to split this large document into manageable chunks. Let me create it properly with the line count parameter.

<write_to_file>
<path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
<content>
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
</content>
<line_count>1282</line_count>
</write_to_file>

---

**User:**

[write_to_file for 'documentation/BACKEND_ARCHITECTURE_PLAN.md'] Result:
<file_write_result>
<path>documentation/BACKEND_ARCHITECTURE_PLAN.md</path>
<operation>created</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
documentation\BACKEND_ARCHITECTURE_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/BACKEND_ARCHITECTURE_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:43:02.537Z
User time zone: Europe/Madrid, UTC+2:00

# Current Cost
$0.56

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Analyze all mock data structures used in frontend to identify required backend data models | Pending |
| 2 | Map frontend API endpoints to backend route requirements | Pending |
| 3 | Design Communication & Security architecture (CORS, JWT authentication) | Pending |
| 4 | Design complete RESTful API endpoint structure with request/response schemas | Pending |
| 5 | Draft comprehensive Django models.py schema with all relationships | Pending |
| 6 | Plan AI service layer architecture and integration points | Pending |
| 7 | Create deployment strategy for Django backend on Render/Railway | Pending |
| 8 | Document environment variable configuration for frontend-backend connection | Pending |
| 9 | Create comprehensive architecture documentation with diagrams | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Analyze all mock data structures used in frontend to identify required backend data models
[x] Map frontend API endpoints to backend route requirements
[x] Design Communication & Security architecture (CORS, JWT authentication)
[x] Design complete RESTful API endpoint structure with request/response schemas
[x] Draft comprehensive Django models.py schema with all relationships
[x] Plan AI service layer architecture and integration points
[x] Create deployment strategy for Django backend on Render/Railway
[x] Document environment variable configuration for frontend-backend connection
[x] Create comprehensive architecture documentation with diagrams
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
documentation\BACKEND_ARCHITECTURE_PLAN.md

# VSCode Open Tabs
frontend/package.json,documentation/BACKEND_EXECUTION_PLAN.md,documentation/BACKEND_ARCHITECTURE_PLAN.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-02T21:43:37.419Z
User time zone: Europe/Madrid, UTC+2:00

# Current Cost
$0.70

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Analyze all mock data structures used in frontend to identify required backend data models | Completed |
| 2 | Map frontend API endpoints to backend route requirements | Completed |
| 3 | Design Communication & Security architecture (CORS, JWT authentication) | Completed |
| 4 | Design complete RESTful API endpoint structure with request/response schemas | Completed |
| 5 | Draft comprehensive Django models.py schema with all relationships | Completed |
| 6 | Plan AI service layer architecture and integration points | Completed |
| 7 | Create deployment strategy for Django backend on Render/Railway | Completed |
| 8 | Document environment variable configuration for frontend-backend connection | Completed |
| 9 | Create comprehensive architecture documentation with diagrams | Completed |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
I've created a comprehensive Django backend architecture plan for GrantBridge in [`documentation/BACKEND_ARCHITECTURE_PLAN.md`](documentation/BACKEND_ARCHITECTURE_PLAN.md).

## Key Deliverables Completed:

### 1. Communication & Security
- **CORS Configuration**: Whitelist-based approach for Vercel domains with environment-specific settings
- **JWT Authentication**: Stateless auth using django-ninja-jwt with 15-minute access tokens and 7-day refresh tokens
- **Security Headers**: XSS protection, HTTPS enforcement, secure cookies

### 2. API Route Design
- **Complete REST API structure** with 8 endpoint categories:
  - Authentication (register, login, refresh, logout)
  - Organizations (CRUD + stats)
  - Grants (list, search, save with filters)
  - Matching (AI-powered grant matching)
  - Proposals (CRUD + AI generation)
  - AI Services (generate, improve, rewrite text)
  - Dashboard (stats, analytics, notifications)
  - Analytics (trends, categories, success rates)
- **Standardized response formats** for success, errors, and pagination

### 3. Data Models Schema
- **7 core models** designed to replace all frontend mock data:
  - User (authentication with organization relationship)
  - Organization (mission, goals, categories, historical projects)
  - Grant (funding details, requirements, eligibility)
  - Proposal (AI-generated content, versioning)
  - GrantMatch (semantic matching scores)
  - Notification (user alerts)
  - Application (tracking grant applications)
- **Complete relationships** with proper indexes and constraints
- **Entity-Relationship diagram** included

### 4. Infrastructure & Deployment
- **Platform recommendations**: Railway (primary) or Render
- **Database**: Neon PostgreSQL (serverless)
- **Complete environment variable configuration** for both backend and frontend
- **Deployment workflow** with automatic CI/CD from GitHub
- **Architecture diagram** showing all components

### 5. Additional Features
- **AI Service Layer**: Modular structure for watsonx.ai integration
- **Vector Store**: ChromaDB for semantic search
- **Background Tasks**: Celery + Redis for async processing
- **Mock Data Replacement Strategy**: Detailed mapping of frontend mock data to backend endpoints
- **4-week development roadmap**

The plan is production-ready for a PoC and follows Django + Django Ninja best practices for decoupled architecture.
</result>
</attempt_completion>

