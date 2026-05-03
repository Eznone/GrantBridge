/**
 * Authentication Service
 * Handles all authentication-related API calls
 */

import { apiClient } from './api-client'
import API_ENDPOINTS from '@/lib/constants/api-endpoints'
import { User, AuthResponse, LoginCredentials, RegisterData } from '@/types/user'

export const authService = {
  /**
   * Login user
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    // Note: The backend uses 'access' instead of 'token' based on API_DOCUMENTATION.md
    // and Ninja JWT defaults.
    const response = await apiClient.post<any>(API_ENDPOINTS.AUTH.LOGIN, credentials)
    
    // Normalize response for frontend
    return {
      user: response.user,
      token: response.access,
      refreshToken: response.refresh
    }
  },

  /**
   * Register user
   */
  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await apiClient.post<any>(API_ENDPOINTS.AUTH.REGISTER, data)
    
    return {
      user: response.user,
      token: response.access,
      refreshToken: response.refresh
    }
  },

  /**
   * Get current user profile
   */
  async getMe(): Promise<User> {
    return apiClient.get<User>('/auth/me')
  },

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    const refreshToken = localStorage.getItem('refresh_token')
    if (refreshToken) {
      try {
        await apiClient.post(API_ENDPOINTS.AUTH.LOGOUT, { refresh: refreshToken })
      } catch (error) {
        console.error('Logout failed:', error)
      }
    }
  },

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<{ access: string }> {
    const refreshToken = localStorage.getItem('refresh_token')
    return apiClient.post<{ access: string }>(API_ENDPOINTS.AUTH.REFRESH, { refresh: refreshToken })
  }
}

// Made with Bob
