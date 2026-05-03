/**
 * Grant Service
 * Handles all grant-related API calls
 */

import { apiClient } from './api-client'
import API_ENDPOINTS from '@/lib/constants/api-endpoints'
import { Grant } from '@/types/grant'
import { PaginatedResponse } from '@/types/api'

export interface GrantFilters {
  page?: number
  page_size?: number
  search?: string
  categories?: string
  tags?: string
  min_amount?: number
  max_amount?: number
  deadline_from?: string
  deadline_to?: string
  geographic_scope?: string
  sort_by?: string
}

export interface GrantListResponse {
  grants: Grant[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export const grantService = {
  /**
   * List grants with filters
   */
  async listGrants(filters?: GrantFilters): Promise<GrantListResponse> {
    return apiClient.get<GrantListResponse>(API_ENDPOINTS.GRANTS.BASE, filters)
  },

  /**
   * Get a single grant by ID
   */
  async getGrant(id: string): Promise<Grant> {
    return apiClient.get<Grant>(API_ENDPOINTS.GRANTS.BY_ID(id))
  },

  /**
   * Search grants
   */
  async searchGrants(query: string, filters?: GrantFilters): Promise<GrantListResponse> {
    return apiClient.get<GrantListResponse>(API_ENDPOINTS.GRANTS.SEARCH, {
      search: query,
      ...filters,
    })
  },

  /**
   * Save/bookmark a grant
   */
  async saveGrant(grantId: string, notes?: string): Promise<any> {
    return apiClient.post(`/grants/${grantId}/save`, { notes })
  },

  /**
   * Unsave/unbookmark a grant
   */
  async unsaveGrant(grantId: string): Promise<any> {
    return apiClient.delete(`/grants/${grantId}/save`)
  },

  /**
   * Get saved grants
   */
  async getSavedGrants(): Promise<Grant[]> {
    return apiClient.get<Grant[]>('/grants/saved')
  },

  /**
   * Get applications
   */
  async getApplications(status?: string): Promise<any[]> {
    return apiClient.get<any[]>('/applications', { status })
  },

  /**
   * Get application by ID
   */
  async getApplication(id: string): Promise<any> {
    return apiClient.get<any>(`/applications/${id}`)
  },
}

// Made with Bob