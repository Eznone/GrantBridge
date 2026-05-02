const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export const API_ENDPOINTS = {
  // Authentication
  AUTH: {
    LOGIN: `${API_BASE}/auth/login`,
    REGISTER: `${API_BASE}/auth/register`,
    REFRESH: `${API_BASE}/auth/refresh`,
    LOGOUT: `${API_BASE}/auth/logout`,
  },
  
  // Organizations
  ORGANIZATIONS: {
    BASE: `${API_BASE}/organizations`,
    BY_ID: (id: string) => `${API_BASE}/organizations/${id}`,
  },
  
  // Grants
  GRANTS: {
    BASE: `${API_BASE}/grants`,
    BY_ID: (id: string) => `${API_BASE}/grants/${id}`,
    SEARCH: `${API_BASE}/grants/search`,
  },
  
  // Matching
  MATCHING: {
    BASE: `${API_BASE}/matching`,
    BY_ORG: (orgId: string) => `${API_BASE}/matching/${orgId}`,
  },
  
  // Proposals
  PROPOSALS: {
    BASE: `${API_BASE}/proposals`,
    BY_ID: (id: string) => `${API_BASE}/proposals/${id}`,
  },
  
  // AI Services
  AI: {
    GENERATE_PROPOSAL: `${API_BASE}/ai/generate-proposal`,
    IMPROVE_TEXT: `${API_BASE}/ai/improve-text`,
    REWRITE: `${API_BASE}/ai/rewrite`,
    ADJUST_TONE: `${API_BASE}/ai/adjust-tone`,
  },
  
  // Dashboard
  DASHBOARD: {
    STATS: `${API_BASE}/dashboard/stats`,
  },
} as const

export default API_ENDPOINTS

// Made with Bob
