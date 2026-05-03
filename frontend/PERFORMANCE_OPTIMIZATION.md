# Frontend Performance Optimization Guide

## Current Performance Issues

### Compilation Times (Development)
- Initial compile: ~15-19 seconds
- Route changes: 3-12 seconds
- Module count: 2400+ modules

### Root Causes
1. **Large dependency tree** - Framer Motion, Recharts, Tiptap add significant bundle size
2. **No code splitting** - All components loaded upfront
3. **Heavy re-renders** - Some components re-render unnecessarily
4. **Development mode overhead** - Next.js dev server compiles on-demand

## Optimization Strategies

### 1. Dynamic Imports ✅
Use Next.js dynamic imports for heavy components:

```typescript
// Instead of:
import { AnalyticsOverview } from '@/components/dashboard/analytics-overview'

// Use:
const AnalyticsOverview = dynamic(() => 
  import('@/components/dashboard/analytics-overview').then(mod => ({ default: mod.AnalyticsOverview })),
  { loading: () => <LoadingSpinner /> }
)
```

**Apply to:**
- Recharts components (analytics-overview.tsx)
- Tiptap editor (tiptap-editor.tsx)
- AI suggestions (ai-suggestions.tsx)
- Large page components

### 2. React.memo for Expensive Components
Prevent unnecessary re-renders:

```typescript
export const ExpensiveComponent = React.memo(({ data }) => {
  // Component logic
}, (prevProps, nextProps) => {
  // Custom comparison
  return prevProps.data.id === nextProps.data.id
})
```

### 3. Optimize Framer Motion
Use `LazyMotion` for smaller bundle:

```typescript
import { LazyMotion, domAnimation, m } from 'framer-motion'

<LazyMotion features={domAnimation}>
  <m.div animate={{ opacity: 1 }}>Content</m.div>
</LazyMotion>
```

### 4. Code Splitting by Route
Next.js already does this, but ensure:
- Each page is in its own file
- Shared components are in separate files
- No circular dependencies

### 5. Optimize Dependencies

**Current Heavy Dependencies:**
- `framer-motion` (~100KB)
- `recharts` (~400KB)
- `@tiptap/*` (~200KB)
- `zustand` (small, ~3KB)

**Alternatives to Consider:**
- Replace Recharts with lighter library (Chart.js, Victory)
- Use CSS animations instead of Framer Motion where possible
- Lazy load Tiptap only on proposal page

### 6. Next.js Configuration

**next.config.js optimizations:**
```javascript
module.exports = {
  // Enable SWC minification (faster)
  swcMinify: true,
  
  // Optimize images
  images: {
    domains: [],
    formats: ['image/avif', 'image/webp'],
  },
  
  // Reduce bundle size
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
  
  // Experimental features
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['recharts', 'framer-motion', '@tiptap/react'],
  },
}
```

### 7. Webpack Bundle Analyzer

**Install:**
```bash
npm install --save-dev @next/bundle-analyzer
```

**Configure:**
```javascript
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({
  // your config
})
```

**Run:**
```bash
ANALYZE=true npm run build
```

### 8. Production Build Optimizations

**These only apply in production:**
- Tree shaking removes unused code
- Minification reduces file size
- Static optimization for pages
- Image optimization
- Font optimization

### 9. Development Experience Improvements

**Turbopack (Next.js 13+):**
```bash
npm run dev -- --turbo
```

**Reduce Module Resolution:**
- Use barrel exports sparingly
- Import directly from files when possible
- Avoid deep imports from node_modules

### 10. Caching Strategies

**Browser Caching:**
```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/:all*(svg|jpg|png)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ]
  },
}
```

## Implementation Priority

### High Priority (Immediate Impact)
1. ✅ Dynamic imports for Recharts
2. ✅ Dynamic imports for Tiptap
3. ✅ Optimize next.config.js
4. ✅ Use LazyMotion

### Medium Priority (Moderate Impact)
5. React.memo for expensive components
6. Optimize Framer Motion usage
7. Bundle analyzer review
8. Remove unused dependencies

### Low Priority (Minor Impact)
9. CSS animations instead of JS where possible
10. Image optimization
11. Font optimization

## Expected Improvements

### After Optimizations:
- **Initial compile:** 8-10 seconds (50% faster)
- **Route changes:** 1-3 seconds (70% faster)
- **Production bundle:** 30-40% smaller
- **First contentful paint:** 40% faster
- **Time to interactive:** 50% faster

## Monitoring

### Development Metrics
```bash
# Check bundle size
npm run build

# Analyze bundle
ANALYZE=true npm run build

# Check compilation time
time npm run dev
```

### Production Metrics
- Lighthouse scores
- Core Web Vitals
- Bundle size reports
- Server response times

## Best Practices Going Forward

1. **Lazy load heavy components** - Use dynamic imports
2. **Optimize images** - Use Next.js Image component
3. **Minimize dependencies** - Only add what's necessary
4. **Code split by route** - Keep pages independent
5. **Use React.memo** - For expensive renders
6. **Profile regularly** - Use React DevTools Profiler
7. **Monitor bundle size** - Set size budgets
8. **Test on slow devices** - Don't just test on fast machines

## Quick Wins

### Immediate Actions (5 minutes):
```bash
# 1. Update next.config.js with optimizations
# 2. Add dynamic imports to heavy components
# 3. Enable Turbopack for dev
npm run dev -- --turbo
```

### Short Term (1 hour):
- Implement LazyMotion
- Add React.memo to expensive components
- Run bundle analyzer
- Remove unused dependencies

### Long Term (1 day):
- Refactor to use lighter alternatives
- Implement proper code splitting
- Add performance monitoring
- Set up CI/CD performance budgets

---

**Note:** Development mode will always be slower than production. The optimizations above focus on both, but production builds will see the most dramatic improvements.