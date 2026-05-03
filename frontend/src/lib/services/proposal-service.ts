/**
 * Proposal Service
 * Handles all proposal-related API calls
 */

import { apiClient } from './api-client'
import API_ENDPOINTS from '@/lib/constants/api-endpoints'
import { Proposal } from '@/types/proposal'

export interface ProposalFilters {
  status?: string
  grant_id?: string
  ai_generated?: boolean
  search?: string
  page?: number
  page_size?: number
}

export interface CreateProposalData {
  grant_id: string
  title: string
  content?: string
}

export interface UpdateProposalData {
  title?: string
  content?: string
  status?: string
}

export const proposalService = {
  /**
   * List proposals with filters
   */
  async listProposals(filters?: ProposalFilters): Promise<Proposal[]> {
    return apiClient.get<Proposal[]>(API_ENDPOINTS.PROPOSALS.BASE, filters)
  },

  /**
   * Get a single proposal by ID
   */
  async getProposal(id: string): Promise<Proposal> {
    return apiClient.get<Proposal>(API_ENDPOINTS.PROPOSALS.BY_ID(id))
  },

  /**
   * Create a new proposal
   */
  async createProposal(data: CreateProposalData): Promise<Proposal> {
    return apiClient.post<Proposal>(API_ENDPOINTS.PROPOSALS.BASE, data)
  },

  /**
   * Update a proposal
   */
  async updateProposal(id: string, data: UpdateProposalData): Promise<Proposal> {
    return apiClient.put<Proposal>(API_ENDPOINTS.PROPOSALS.BY_ID(id), data)
  },

  /**
   * Partially update a proposal
   */
  async patchProposal(id: string, data: Partial<UpdateProposalData>): Promise<Proposal> {
    return apiClient.patch<Proposal>(API_ENDPOINTS.PROPOSALS.BY_ID(id), data)
  },

  /**
   * Delete a proposal
   */
  async deleteProposal(id: string): Promise<void> {
    return apiClient.delete<void>(API_ENDPOINTS.PROPOSALS.BY_ID(id))
  },

  /**
   * Submit a proposal
   */
  async submitProposal(id: string, submissionMethod: string): Promise<Proposal> {
    return apiClient.post<Proposal>(`/proposals/${id}/submit`, {
      submission_method: submissionMethod,
    })
  },

  /**
   * Create a new version of a proposal
   */
  async createVersion(id: string): Promise<Proposal> {
    return apiClient.post<Proposal>(`/proposals/${id}/version`)
  },

  /**
   * Get proposal versions
   */
  async getVersions(id: string): Promise<any[]> {
    return apiClient.get<any[]>(`/proposals/${id}/versions`)
  },

  /**
   * Export proposal
   */
  async exportProposal(id: string, format: 'pdf' | 'docx'): Promise<Blob> {
    return apiClient.postBlob(`${API_ENDPOINTS.PROPOSALS.BY_ID(id)}/export`, { format })
  },

  /**
   * Get proposal statistics
   */
  async getStats(): Promise<any> {
    return apiClient.get<any>('/proposals/stats')
  },
}

// Made with Bob