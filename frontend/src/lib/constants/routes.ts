export const ROUTES = {
  // Public routes
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  
  // Dashboard routes
  DASHBOARD: '/',
  GRANTS: '/grants',
  APPLICATIONS: '/applications',
  PROPOSALS: '/proposals',
  AI_ASSISTANT: '/ai-assistant',
  PROFILE: '/profile',
  SETTINGS: '/settings',
  
  // Dynamic routes
  GRANT_DETAIL: (id: string) => `/grants/${id}`,
  PROPOSAL_DETAIL: (id: string) => `/proposals/${id}`,
  PROPOSAL_EDIT: (id: string) => `/proposals/${id}/edit`,
} as const

export type RouteKey = keyof typeof ROUTES

// Made with Bob
