/**
 * Matching Service
 * Handles all grant matching-related API calls
 */

import { apiClient } from './api-client'

export interface GrantMatch {
  id: string
  grant_id: string
  grant_title: string
  grant_description: string
  match_score: number
  quality: string
  reasoning: string[]
  is_dismissed: boolean
  created_at: string
}

export interface MatchStats {
  total_matches: number
  excellent_matches: number
  good_matches: number
  fair_matches: number
  average_score: number
}

export interface CalculateMatchesResponse {
  matches_created: number
  matches_updated: number
  total_matches: number
}

export const matchingService = {
  /**
   * Get grant matches
   */
  async getMatches(filters?: {
    min_score?: number
    max_score?: number
    quality?: string
    include_dismissed?: boolean
    limit?: number
  }): Promise<GrantMatch[]> {
    return apiClient.get<GrantMatch[]>('/matches', filters)
  },

  /**
   * Get a single match by ID
   */
  async getMatch(id: string): Promise<GrantMatch> {
    return apiClient.get<GrantMatch>(`/matches/${id}`)
  },

  /**
   * Dismiss a match
   */
  async dismissMatch(id: string, reason?: string): Promise<GrantMatch> {
    return apiClient.post<GrantMatch>(`/matches/${id}/dismiss`, { reason })
  },

  /**
   * Restore a dismissed match
   */
  async undismissMatch(id: string): Promise<GrantMatch> {
    return apiClient.post<GrantMatch>(`/matches/${id}/undismiss`)
  },

  /**
   * Calculate matches for the organization
   */
  async calculateMatches(data?: {
    grant_ids?: string[]
    force_recalculate?: boolean
  }): Promise<CalculateMatchesResponse> {
    return apiClient.post<CalculateMatchesResponse>('/matches/calculate', data)
  },

  /**
   * Get match statistics
   */
  async getMatchStats(): Promise<MatchStats> {
    return apiClient.get<MatchStats>('/matches/stats')
  },

  /**
   * Get top matches
   */
  async getTopMatches(limit: number = 10): Promise<GrantMatch[]> {
    return apiClient.get<GrantMatch[]>('/matches/top', { limit })
  },
}

// Made with Bob