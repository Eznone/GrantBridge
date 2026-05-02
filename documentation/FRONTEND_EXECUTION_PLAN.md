# Frontend Development Execution Plan
## AI Grant Assistant - Step-by-Step Implementation Guide

---

## 📋 Quick Reference

**Total Timeline:** 10 days (hackathon-optimized)  
**Approach:** Incremental development with testable milestones  
**Tech Stack:** Next.js 14, TypeScript, Tailwind CSS, shadcn/ui, React Query, Zustand

---

## 🚀 Phase 1: Foundation (Days 1-2)

### Step 1: Project Setup
```bash
# Initialize project
npx create-next-app@latest grantbridge-frontend --typescript --tailwind --app --src-dir
cd grantbridge-frontend

# Install dependencies
npm install @tanstack/react-query axios zustand lucide-react
npm install class-variance-authority clsx tailwind-merge
npm install react-hook-form @hookform/resolvers zod date-fns next-themes

# Setup shadcn/ui
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card input label dialog dropdown-menu avatar badge separator tooltip tabs progress skeleton
```

**Create Structure:**
```bash
mkdir -p src/{lib/{api,hooks,stores,utils,constants},types,components/{layout,kanban,grants,proposals,ai,analytics,shared}}
mkdir -p src/app/\(auth\)/{login,register}
mkdir -p src/app/\(dashboard\)/{grants,applications,proposals,ai-assistant,profile,settings}
```

**Key Files:**
- `src/lib/constants/routes.ts` - Route definitions
- `src/lib/constants/api-endpoints.ts` - API endpoint constants
- `src/types/*.ts` - TypeScript interfaces (User, Grant, Proposal, Organization)
- `src/lib/api/client.ts` - Axios client with interceptors
- `src/lib/providers/query-provider.tsx` - React Query setup

**Deliverable:** ✅ Working Next.js app with all dependencies

---

### Step 2: Authentication System
**Files to Create:**
- `src/lib/stores/auth-store.ts` - Zustand auth store
- `src/app/(auth)/login/page.tsx` - Login page
- `src/app/(auth)/register/page.tsx` - Register page
- `src/components/auth/protected-route.tsx` - Route protection

**Key Features:**
- JWT token management
- Persistent auth state
- Login/register forms
- Error handling

**Deliverable:** ✅ Complete auth flow with protected routes

---

### Step 3: Layout & Navigation
**Files to Create:**
- `src/components/layout/sidebar.tsx` - Collapsible sidebar
- `src/components/layout/topbar.tsx` - Top navigation with user menu
- `src/app/(dashboard)/layout.tsx` - Dashboard layout wrapper

**Features:**
- Sidebar with 7 navigation items
- Theme toggle (light/dark)
- User dropdown menu
- Search bar
- Responsive design

**Deliverable:** ✅ Complete dashboard shell

---

## 📊 Phase 2: Dashboard & Data (Days 3-4)

### Step 4: Dashboard Page
**Files to Create:**
- `src/lib/api/dashboard.ts` - Dashboard API hooks
- `src/components/analytics/metric-card.tsx` - Metric display component
- `src/app/(dashboard)/page.tsx` - Dashboard page

**Components:**
- 4 metric cards (Active Apps, Funding, Match Rate, Proposals)
- 2 chart placeholders
- Recent activity sections

**Deliverable:** ✅ Functional dashboard with metrics

---

### Step 5: Grant API Integration
**Files to Create:**
- `src/lib/api/grants.ts` - Grant CRUD hooks
- `src/components/grants/grant-card.tsx` - Grant display card
- `src/components/grants/match-score-badge.tsx` - Score visualization

**Hooks:**
- `useGrants(filters)` - Fetch grants
- `useGrant(id)` - Single grant
- `useUpdateGrantStatus()` - Update status

**Deliverable:** ✅ Grant data management ready

---

## 🎯 Phase 3: Kanban Board (Days 5-6)

### Step 6: Kanban Setup
```bash
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
```

**Files to Create:**
- `src/components/kanban/board.tsx` - Main board component
- `src/components/kanban/column.tsx` - Kanban column
- `src/components/kanban/card.tsx` - Draggable grant card
- `src/app/(dashboard)/applications/page.tsx` - Applications page

**Columns:**
1. Opportunities Found
2. Reviewing
3. Drafting Proposal
4. Submitted

**Features:**
- Drag and drop cards between columns
- Status updates via API
- Match score badges
- Deadline indicators
- Funding amounts

**Deliverable:** ✅ Fully functional Kanban board

---

### Step 7: Grant Discovery
**Files to Create:**
- `src/app/(dashboard)/grants/page.tsx` - Grant list page
- `src/components/grants/grant-list.tsx` - List view
- `src/components/grants/grant-filters.tsx` - Filter controls

**Features:**
- Search functionality
- Filter by amount, tags, deadline
- Sort by match score
- Grid/list view toggle

**Deliverable:** ✅ Grant discovery interface

---

## ✍️ Phase 4: AI Proposal Editor (Days 7-8)

### Step 8: Editor Setup
```bash
npm install @tiptap/react @tiptap/starter-kit @tiptap/extension-placeholder
```

**Files to Create:**
- `src/lib/api/proposals.ts` - Proposal API hooks
- `src/lib/api/ai.ts` - AI generation hooks
- `src/components/proposals/proposal-editor.tsx` - Main editor
- `src/components/proposals/ai-toolbar.tsx` - AI action buttons
- `src/app/(dashboard)/proposals/[id]/page.tsx` - Editor page

**AI Features:**
- Generate full proposal
- Rewrite selection
- Expand/shorten text
- Adjust tone (professional, persuasive, concise)
- Auto-save every 2 seconds

**Deliverable:** ✅ AI-powered proposal editor

---

### Step 9: AI Loading States
**Files to Create:**
- `src/components/ai/ai-loading-state.tsx` - Contextual loading
- `src/components/ai/ai-suggestion-card.tsx` - Suggestion display

**Loading Messages:**
- "Analyzing grant requirements..."
- "Generating proposal structure..."
- "Calculating organization compatibility..."
- "Enhancing proposal clarity..."

**Deliverable:** ✅ Polished AI interactions

---

## 🎨 Phase 5: Polish & Enhancement (Days 9-10)

### Step 10: Animations
```bash
npm install framer-motion
```

**Add to:**
- Modal transitions
- Card hover effects
- Drag interactions
- AI loading states

**Deliverable:** ✅ Smooth, premium animations

---

### Step 11: Charts & Analytics
```bash
npm install recharts
```

**Files to Create:**
- `src/components/analytics/funding-chart.tsx` - Bar chart
- `src/components/analytics/progress-chart.tsx` - Pie/donut chart

**Update:** Dashboard page with real charts

**Deliverable:** ✅ Visual analytics

---

### Step 12: Organization Profile
**Files to Create:**
- `src/app/(dashboard)/profile/page.tsx` - Profile page
- `src/lib/api/organizations.ts` - Organization API

**Features:**
- Edit mission statement
- Manage categories
- Add historical projects
- Set funding needs

**Deliverable:** ✅ Organization management

---

### Step 13: Error & Empty States
**Files to Create:**
- `src/components/shared/error-state.tsx` - Error display
- `src/components/shared/empty-state.tsx` - Empty list display
- `src/components/shared/loading-skeleton.tsx` - Loading placeholders

**Apply to:** All list views and data displays

**Deliverable:** ✅ Comprehensive UX states

---

### Step 14: Final Polish
**Tasks:**
- [ ] Test all user flows
- [ ] Verify responsive design (desktop, tablet)
- [ ] Test dark mode throughout
- [ ] Fix any bugs
- [ ] Optimize performance
- [ ] Add loading skeletons everywhere
- [ ] Verify accessibility (keyboard navigation)
- [ ] Test error handling
- [ ] Prepare demo data

**Deliverable:** ✅ Production-ready MVP

---

## 📝 Implementation Checklist

### Foundation ✅
- [ ] Project initialized
- [ ] Dependencies installed
- [ ] shadcn/ui configured
- [ ] Folder structure created
- [ ] TypeScript types defined
- [ ] API client setup
- [ ] React Query configured

### Authentication ✅
- [ ] Auth store created
- [ ] Login page
- [ ] Register page
- [ ] Protected routes
- [ ] Token management

### Layout ✅
- [ ] Sidebar navigation
- [ ] Topbar with user menu
- [ ] Theme toggle
- [ ] Dashboard layout

### Dashboard ✅
- [ ] Metric cards
- [ ] Charts (Recharts)
- [ ] Recent activity
- [ ] Loading states

### Kanban ✅
- [ ] dnd-kit setup
- [ ] Board component
- [ ] 4 columns
- [ ] Draggable cards
- [ ] Status updates
- [ ] Match score badges

### Grants ✅
- [ ] Grant list page
- [ ] Grant cards
- [ ] Filters
- [ ] Search
- [ ] Detail view

### Proposals ✅
- [ ] Tiptap editor
- [ ] AI toolbar
- [ ] Generate proposal
- [ ] Rewrite/improve
- [ ] Tone adjustment
- [ ] Auto-save

### AI Integration ✅
- [ ] Loading states
- [ ] Error handling
- [ ] Contextual messages
- [ ] Suggestion cards

### Polish ✅
- [ ] Framer Motion animations
- [ ] Charts
- [ ] Organization profile
- [ ] Error states
- [ ] Empty states
- [ ] Loading skeletons

---

## 🔧 Key Code Patterns

### API Hook Pattern
```typescript
export function useGrants(filters?: GrantFilters) {
  return useQuery({
    queryKey: ['grants', filters],
    queryFn: async () => {
      const { data } = await apiClient.get('/grants', { params: filters })
      return data
    },
  })
}
```

### Mutation Pattern
```typescript
export function useUpdateGrant() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (grant: Grant) => {
      const { data } = await apiClient.put(`/grants/${grant.id}`, grant)
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['grants'] })
    },
  })
}
```

### Component Pattern
```typescript
'use client'

import { useGrants } from '@/lib/api/grants'
import { GrantCard } from '@/components/grants/grant-card'
import { Skeleton } from '@/components/ui/skeleton'

export function GrantList() {
  const { data: grants, isLoading, error } = useGrants()

  if (isLoading) return <Skeleton className="h-64" />
  if (error) return <ErrorState error={error} />
  if (!grants?.length) return <EmptyState />

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {grants.map((grant) => (
        <GrantCard key={grant.id} grant={grant} />
      ))}
    </div>
  )
}
```

---

## 🎯 Daily Goals

### Day 1: Setup
- Project initialization
- Dependencies
- Folder structure
- Type definitions

### Day 2: Auth & Layout
- Authentication system
- Sidebar & topbar
- Dashboard layout

### Day 3: Dashboard
- Metric cards
- API integration
- Loading states

### Day 4: Grant Management
- Grant API hooks
- Grant cards
- Filters

### Day 5: Kanban Part 1
- dnd-kit setup
- Board structure
- Columns

### Day 6: Kanban Part 2
- Drag and drop
- Status updates
- Polish

### Day 7: Editor Setup
- Tiptap integration
- Basic editor
- Auto-save

### Day 8: AI Integration
- AI toolbar
- Generation
- Improvements

### Day 9: Polish
- Animations
- Charts
- Profile

### Day 10: Final
- Testing
- Bug fixes
- Demo prep

---

## 🚨 Common Issues & Solutions

### Issue: CORS errors
**Solution:** Ensure backend has proper CORS headers

### Issue: Auth token not persisting
**Solution:** Check localStorage and Zustand persist config

### Issue: Drag and drop not working
**Solution:** Verify dnd-kit sensors and collision detection

### Issue: Dark mode flickering
**Solution:** Use `suppressHydrationWarning` on html tag

### Issue: API calls failing
**Solution:** Check API_URL in .env.local

---

## ✅ Definition of Done

Each feature is complete when:
1. ✅ Functionality works as specified
2. ✅ TypeScript types are defined
3. ✅ Loading states implemented
4. ✅ Error handling in place
5. ✅ Responsive design (desktop + tablet)
6. ✅ Dark mode supported
7. ✅ No console errors
8. ✅ Tested manually

---

## 🎉 Success Criteria

**MVP is ready when:**
- ✅ User can login/register
- ✅ Dashboard shows metrics
- ✅ Kanban board works with drag-and-drop
- ✅ Grants can be discovered and filtered
- ✅ AI can generate proposals
- ✅ Proposals can be edited with AI assistance
- ✅ Dark mode works throughout
- ✅ No critical bugs
- ✅ Demo-ready with sample data

---

**Document Version:** 1.0  
**Last Updated:** 2026-05-02  
**Status:** Ready for Implementation