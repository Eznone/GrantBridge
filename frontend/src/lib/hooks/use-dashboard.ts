/**
 * Custom hooks for dashboard data fetching
 */

import { useState, useEffect } from 'react'
import { dashboardService, DashboardStats, UpcomingDeadline } from '@/lib/services/dashboard-service'

export function useDashboardStats() {
  const [data, setData] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true

    async function fetchStats() {
      try {
        setLoading(true)
        setError(null)
        const result = await dashboardService.getStats()
        if (mounted) {
          setData(result)
        }
      } catch (err: any) {
        if (mounted) {
          setError(err.message || 'Failed to fetch dashboard stats')
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    fetchStats()

    return () => {
      mounted = false
    }
  }, [])

  return { data, loading, error }
}

export function useUpcomingDeadlines(days: number = 30) {
  const [data, setData] = useState<UpcomingDeadline[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true

    async function fetchDeadlines() {
      try {
        setLoading(true)
        setError(null)
        const result = await dashboardService.getUpcomingDeadlines(days)
        if (mounted) {
          setData(result)
        }
      } catch (err: any) {
        if (mounted) {
          setError(err.message || 'Failed to fetch deadlines')
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    fetchDeadlines()

    return () => {
      mounted = false
    }
  }, [days])

  return { data, loading, error }
}

// Made with Bob