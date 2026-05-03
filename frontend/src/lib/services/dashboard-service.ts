/**
 * Dashboard Service
 * Handles all dashboard and analytics-related API calls
 */

import { apiClient } from './api-client'
import API_ENDPOINTS from '@/lib/constants/api-endpoints'

export interface DashboardStats {
  total_proposals: number
  active_applications: number
  saved_grants: number
  pending_matches: number
  success_rate: number
  total_funding: number
}

export interface UpcomingDeadline {
  grant_id: string
  grant_title: string
  deadline: string
  days_remaining: number
  application_id?: string
  is_saved: boolean
}

export interface Notification {
  id: number
  type: string
  title: string
  message: string
  is_read: boolean
  created_at: string
  related_object_id?: string
}

export interface AnalyticsTrends {
  labels: string[]
  proposals: number[]
  applications: number[]
  matches: number[]
}

export interface AnalyticsCategories {
  categories: string[]
  applications: number[]
  success_rates: number[]
}

export interface AnalyticsSuccessRate {
  overall_rate: number
  by_category: Record<string, number>
  by_amount: Record<string, number>
}

export interface AnalyticsFunding {
  total_requested: number
  total_awarded: number
  total_pending: number
  by_status: Record<string, number>
}

export const dashboardService = {
  /**
   * Get dashboard statistics
   */
  async getStats(): Promise<DashboardStats> {
    return apiClient.get<DashboardStats>(API_ENDPOINTS.DASHBOARD.STATS)
  },

  /**
   * Get upcoming deadlines
   */
  async getUpcomingDeadlines(days: number = 30): Promise<UpcomingDeadline[]> {
    return apiClient.get<UpcomingDeadline[]>('/dashboard/deadlines', { days })
  },

  /**
   * Get notifications
   */
  async getNotifications(unreadOnly: boolean = false): Promise<Notification[]> {
    return apiClient.get<Notification[]>('/notifications', { unread_only: unreadOnly })
  },

  /**
   * Mark notification as read
   */
  async markNotificationRead(id: number): Promise<void> {
    return apiClient.post<void>(`/notifications/${id}/read`)
  },

  /**
   * Mark all notifications as read
   */
  async markAllNotificationsRead(): Promise<void> {
    return apiClient.post<void>('/notifications/read-all')
  },

  /**
   * Delete notification
   */
  async deleteNotification(id: number): Promise<void> {
    return apiClient.delete<void>(`/notifications/${id}`)
  },

  /**
   * Get unread notification count
   */
  async getUnreadCount(): Promise<{ unread_count: number }> {
    return apiClient.get<{ unread_count: number }>('/notifications/unread-count')
  },

  /**
   * Get analytics trends
   */
  async getAnalyticsTrends(days: number = 90): Promise<AnalyticsTrends> {
    return apiClient.get<AnalyticsTrends>('/analytics/trends', { days })
  },

  /**
   * Get analytics by category
   */
  async getAnalyticsCategories(): Promise<AnalyticsCategories> {
    return apiClient.get<AnalyticsCategories>('/analytics/categories')
  },

  /**
   * Get success rate analytics
   */
  async getSuccessRate(): Promise<AnalyticsSuccessRate> {
    return apiClient.get<AnalyticsSuccessRate>('/analytics/success-rate')
  },

  /**
   * Get funding analytics
   */
  async getFundingAnalytics(): Promise<AnalyticsFunding> {
    return apiClient.get<AnalyticsFunding>('/analytics/funding')
  },
}

// Made with Bob