# Quick Start Guide - AI Grant Assistant Frontend

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Node.js 18+
- npm or yarn
- Git

### 1. Clone & Setup
```bash
# Initialize project
npx create-next-app@latest grantbridge-frontend --typescript --tailwind --app --src-dir
cd grantbridge-frontend

# Install all dependencies at once
npm install @tanstack/react-query axios zustand lucide-react \
  class-variance-authority clsx tailwind-merge \
  react-hook-form @hookform/resolvers zod date-fns next-themes \
  @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities \
  @tiptap/react @tiptap/starter-kit @tiptap/extension-placeholder \
  framer-motion recharts

# Setup shadcn/ui
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card input label dialog dropdown-menu \
  avatar badge separator tooltip tabs progress skeleton
```

### 2. Configure Environment
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME=GrantBridge
```

### 3. Create Folder Structure
```bash
mkdir -p src/lib/{api,hooks,stores,utils,constants}
mkdir -p src/types
mkdir -p src/components/{layout,kanban,grants,proposals,ai,analytics,shared}
mkdir -p src/app/\(auth\)/{login,register}
mkdir -p src/app/\(dashboard\)/{grants,applications,proposals,ai-assistant,profile,settings}
```

### 4. Start Development
```bash
npm run dev
# Visit http://localhost:3000
```

---

## 📚 Documentation Index

### Main Documents
1. **[FRONTEND_IMPLEMENTATION_ROADMAP.md](./FRONTEND_IMPLEMENTATION_ROADMAP.md)** - Comprehensive technical roadmap
   - Complete architecture overview
   - Technology stack details
   - Component specifications
   - API integration patterns
   - Design system implementation
   - Best practices and guidelines

2. **[FRONTEND_EXECUTION_PLAN.md](./FRONTEND_EXECUTION_PLAN.md)** - Step-by-step coding guide
   - Sequential implementation steps
   - Day-by-day breakdown
   - Code examples for each step
   - Verification checkpoints
   - Common issues and solutions

3. **[Backend Architecture Spec](./specifications/Ai%20Grant%20Assistant%20Backend%20Architecture%20Spec.pdf)** - Backend reference
   - Django + Ninja API structure
   - Database models
   - AI service layer
   - API endpoints

---

## 🎯 Development Workflow

### Phase 1: Foundation (Days 1-2)
```
Setup → Auth → Layout
```
**Goal:** Working app shell with authentication

### Phase 2: Core Features (Days 3-6)
```
Dashboard → Grants → Kanban Board
```
**Goal:** Functional grant management workflow

### Phase 3: AI Features (Days 7-8)
```
Proposal Editor → AI Integration
```
**Goal:** AI-powered proposal generation

### Phase 4: Polish (Days 9-10)
```
Animations → Charts → Testing
```
**Goal:** Production-ready MVP

---

## 🔑 Key Technologies

| Category | Technology | Purpose |
|----------|-----------|---------|
| Framework | Next.js 14 | React framework with SSR |
| Language | TypeScript | Type safety |
| Styling | Tailwind CSS | Utility-first CSS |
| Components | shadcn/ui | Accessible UI components |
| State | Zustand | Global state management |
| Data Fetching | React Query | Server state management |
| HTTP Client | Axios | API requests |
| Drag & Drop | dnd-kit | Kanban functionality |
| Editor | Tiptap | Rich text editing |
| Charts | Recharts | Data visualization |
| Animations | Framer Motion | Smooth transitions |

---

## 📁 Project Structure

```
src/
├── app/                      # Next.js App Router
│   ├── (auth)/              # Auth pages
│   └── (dashboard)/         # Protected pages
├── components/
│   ├── ui/                  # shadcn/ui components
│   ├── layout/              # Sidebar, Topbar
│   ├── kanban/              # Kanban board
│   ├── grants/              # Grant components
│   ├── proposals/           # Proposal editor
│   ├── ai/                  # AI components
│   └── analytics/           # Charts & metrics
├── lib/
│   ├── api/                 # API hooks
│   ├── stores/              # Zustand stores
│   ├── hooks/               # Custom hooks
│   ├── utils/               # Utilities
│   └── constants/           # Constants
└── types/                   # TypeScript types
```

---

## 🎨 Design System

### Colors
```typescript
Primary: #2563eb (Blue)
Accent: #10b981 (Emerald)
Background: #f8fafc (Light) / #0f172a (Dark)
```

### Typography
```typescript
Font: Inter
Sizes: xs(12px) → 4xl(36px)
```

### Components
- Rounded corners: 8px
- Soft shadows
- Smooth transitions
- Dark mode support

---

## 🔌 API Integration

### Endpoints
```
/api/v1/auth/login
/api/v1/auth/register
/api/v1/grants
/api/v1/proposals
/api/v1/matching
/api/v1/ai/generate-proposal
```

### Usage Pattern
```typescript
// 1. Create API hook
export function useGrants() {
  return useQuery({
    queryKey: ['grants'],
    queryFn: async () => {
      const { data } = await apiClient.get('/grants')
      return data
    },
  })
}

// 2. Use in component
function GrantList() {
  const { data, isLoading } = useGrants()
  // Render grants
}
```

---

## ✅ MVP Feature Checklist

### Must Have
- [x] Authentication (login/register)
- [x] Dashboard with metrics
- [x] Kanban board with drag-and-drop
- [x] Grant discovery and filtering
- [x] AI proposal generation
- [x] Proposal editor with AI tools
- [x] Dark mode
- [x] Responsive design (desktop + tablet)

### Should Have
- [ ] Charts and analytics
- [ ] Organization profile
- [ ] Search functionality
- [ ] Loading skeletons
- [ ] Error states
- [ ] Empty states

### Nice to Have
- [ ] Advanced animations
- [ ] AI chat assistant
- [ ] Export proposals
- [ ] Notification system
- [ ] Settings page

---

## 🐛 Troubleshooting

### Common Issues

**CORS Errors**
```bash
# Ensure backend has CORS headers
# Check API_URL in .env.local
```

**Auth Not Persisting**
```typescript
// Verify Zustand persist config
persist(
  (set) => ({ /* state */ }),
  { name: 'auth-storage' }
)
```

**Dark Mode Flickering**
```typescript
// Add to html tag
<html suppressHydrationWarning>
```

**Build Errors**
```bash
# Clear cache and rebuild
rm -rf .next
npm run build
```

---

## 📞 Resources

### Documentation
- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com)
- [React Query](https://tanstack.com/query/latest)
- [dnd-kit](https://docs.dndkit.com)

### Community
- Next.js Discord
- React Discord
- Tailwind CSS Discord

---

## 🎯 Success Metrics

**Technical**
- Lighthouse score > 90
- Bundle size < 300KB
- Time to Interactive < 3s

**User Experience**
- AI generation < 10s
- Smooth 60fps animations
- Search response < 500ms

**Business**
- User onboarding < 5 min
- Grant matching > 80% accuracy
- Positive AI feedback

---

## 🚀 Next Steps

1. **Read** [FRONTEND_IMPLEMENTATION_ROADMAP.md](./FRONTEND_IMPLEMENTATION_ROADMAP.md) for architecture details
2. **Follow** [FRONTEND_EXECUTION_PLAN.md](./FRONTEND_EXECUTION_PLAN.md) for step-by-step implementation
3. **Start** with Phase 1: Foundation
4. **Build** incrementally, testing each feature
5. **Deploy** to Vercel when ready

---

**Ready to build? Start with the execution plan!** 🎉