export interface User {
  id: string
  email: string
  name: string
  organizationId: string
  role: 'admin' | 'member'
  createdAt: string
}

export interface AuthResponse {
  user: User
  token: string
  refreshToken?: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  name: string
  email: string
  password: string
  organizationName?: string
}

// Made with Bob
