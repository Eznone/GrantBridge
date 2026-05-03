/**
 * API Client for GrantBridge
 * Handles HTTP requests with authentication and error handling
 */

import API_ENDPOINTS from '@/lib/constants/api-endpoints'
import { ApiResponse, ApiError, PaginatedResponse } from '@/types/api'

class ApiClient {
  private baseURL: string

  constructor() {
    this.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
  }

  private async getAuthToken(): Promise<string | null> {
    // Get token from localStorage or auth store
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token')
    }
    return null
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = await this.getAuthToken()
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    }

    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const config: RequestInit = {
      ...options,
      headers,
    }

    try {
      const url = endpoint.startsWith('http') ? endpoint : `${this.baseURL}${endpoint}`
      const response = await fetch(url, config)

      if (!response.ok) {
        const error: ApiError = await response.json().catch(() => ({
          message: response.statusText,
          statusCode: response.status,
        }))
        throw error
      }

      return await response.json()
    } catch (error) {
      if (error instanceof Error) {
        throw {
          message: error.message,
          statusCode: 500,
        } as ApiError
      }
      throw error
    }
  }

  async get<T>(endpoint: string, params?: Record<string, any>): Promise<T> {
    const queryString = params
      ? '?' + new URLSearchParams(
          Object.entries(params).reduce((acc, [key, value]) => {
            if (value !== undefined && value !== null) {
              acc[key] = String(value)
            }
            return acc
          }, {} as Record<string, string>)
        ).toString()
      : ''

    return this.request<T>(`${endpoint}${queryString}`, {
      method: 'GET',
    })
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async patch<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'DELETE',
    })
  }

  async postBlob(endpoint: string, data?: any): Promise<Blob> {
    const token = await this.getAuthToken()
    const url = endpoint.startsWith('http') ? endpoint : `${this.baseURL}${endpoint}`
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    }

    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: data ? JSON.stringify(data) : undefined,
    })

    if (!response.ok) {
      const error: ApiError = await response.json().catch(() => ({
        message: response.statusText,
        statusCode: response.status,
      }))
      throw error
    }

    return response.blob()
  }
}

export const apiClient = new ApiClient()

// Made with Bob