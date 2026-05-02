# GrantBridge Frontend

AI-Powered Grant Assistant for NGOs - Frontend Application

## 📋 Project Status

**Phase:** Foundation Setup Complete ✅  
**Step:** Step 1 from Frontend Execution Plan  
**Next:** Install dependencies and begin implementation

## 🏗️ Architecture Overview

This is a Next.js 14 application with TypeScript, Tailwind CSS, and a modern component-based architecture.

### Technology Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript 5
- **Styling:** Tailwind CSS 3.4
- **Package Manager:** npm

### Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/            # Authentication routes
│   │   ├── (dashboard)/       # Protected dashboard routes
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home page
│   │   └── globals.css        # Global styles
│   ├── components/            # React components
│   │   ├── layout/           # Layout components
│   │   ├── kanban/           # Kanban board
│   │   ├── grants/           # Grant components
│   │   ├── proposals/        # Proposal editor
│   │   ├── ai/               # AI components
│   │   ├── analytics/        # Charts & metrics
│   │   └── shared/           # Shared components
│   ├── lib/
│   │   ├── api/              # API client & hooks
│   │   ├── stores/           # State management
│   │   ├── hooks/            # Custom React hooks
│   │   ├── utils/            # Utility functions
│   │   └── constants/        # Constants & config
│   └── types/                # TypeScript definitions
├── public/                   # Static assets
├── .env.local               # Environment variables
├── next.config.js           # Next.js configuration
├── tailwind.config.ts       # Tailwind configuration
├── tsconfig.json            # TypeScript configuration
└── package.json             # Dependencies
```

## 🎯 Foundation Files Created

### Configuration Files
- ✅ `package.json` - Project dependencies
- ✅ `tsconfig.json` - TypeScript configuration
- ✅ `next.config.js` - Next.js configuration
- ✅ `tailwind.config.ts` - Tailwind CSS configuration
- ✅ `postcss.config.js` - PostCSS configuration
- ✅ `.env.local` - Environment variables
- ✅ `.gitignore` - Git ignore rules

### Type Definitions
- ✅ `src/types/user.ts` - User & auth types
- ✅ `src/types/organization.ts` - Organization types
- ✅ `src/types/grant.ts` - Grant types
- ✅ `src/types/proposal.ts` - Proposal types
- ✅ `src/types/api.ts` - API response types

### Constants
- ✅ `src/lib/constants/routes.ts` - Route definitions
- ✅ `src/lib/constants/api-endpoints.ts` - API endpoints

### Utilities
- ✅ `src/lib/utils/cn.ts` - Class name utility
- ✅ `src/lib/utils/format.ts` - Formatting utilities

### App Structure
- ✅ `src/app/layout.tsx` - Root layout
- ✅ `src/app/page.tsx` - Home page
- ✅ `src/app/globals.css` - Global styles

## 🚀 Next Steps

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Install Additional Packages (as needed)

```bash
# State management & data fetching
npm install @tanstack/react-query axios zustand

# UI components
npm install lucide-react class-variance-authority clsx tailwind-merge

# Forms & validation
npm install react-hook-form @hookform/resolvers zod

# Utilities
npm install date-fns next-themes

# Drag and drop (for Kanban)
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities

# Rich text editor (for proposals)
npm install @tiptap/react @tiptap/starter-kit @tiptap/extension-placeholder

# Charts
npm install recharts

# Animations
npm install framer-motion
```

### 3. Setup shadcn/ui

```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card input label dialog dropdown-menu avatar badge separator tooltip tabs progress skeleton
```

### 4. Start Development Server

```bash
npm run dev
```

Visit `http://localhost:3000` to see the application.

## 📖 Documentation

- **[Frontend Implementation Roadmap](../documentation/FRONTEND_IMPLEMENTATION_ROADMAP.md)** - Complete technical guide
- **[Frontend Execution Plan](../documentation/FRONTEND_EXECUTION_PLAN.md)** - Step-by-step implementation
- **[Quick Start Guide](../documentation/QUICK_START_GUIDE.md)** - Quick reference

## 🎨 Design System

### Colors

**Primary (Blue):**
- 50: #eff6ff
- 500: #2563eb (Main)
- 600: #1d4ed8

**Accent (Emerald):**
- 50: #ecfdf5
- 500: #10b981 (Main)
- 600: #059669

### Typography

- **Font:** Inter
- **Sizes:** xs (12px) to 4xl (36px)

### Component Guidelines

- Rounded corners: 8px
- Soft shadows
- Smooth transitions
- Dark mode support

## 🔧 Environment Variables

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME=GrantBridge
```

## 📝 Development Guidelines

### Code Style

- Use TypeScript for all files
- Follow functional component patterns
- Use hooks for state management
- Keep components small and focused
- Use proper TypeScript types

### File Naming

- Components: PascalCase (e.g., `GrantCard.tsx`)
- Utilities: camelCase (e.g., `formatDate.ts`)
- Types: camelCase (e.g., `user.ts`)
- Constants: UPPER_SNAKE_CASE in files

### Component Structure

```typescript
'use client' // If using client-side features

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import type { Grant } from '@/types/grant'

interface GrantCardProps {
  grant: Grant
  onSelect?: (grant: Grant) => void
}

export function GrantCard({ grant, onSelect }: GrantCardProps) {
  // Component logic
  return (
    // JSX
  )
}
```

## 🧪 Testing

Testing setup will be added in later phases.

## 🚢 Deployment

The application is configured for deployment on Vercel:

```bash
npm run build
```

## 📄 License

Private - GrantBridge Project

---

**Status:** Foundation Complete ✅  
**Ready for:** Phase 2 - Authentication & Layout Implementation