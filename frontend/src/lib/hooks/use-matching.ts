/**
 * Custom hooks for grant matching data fetching
 */

import { useState, useEffect } from 'react'
import { matchingService, GrantMatch, MatchStats } from '@/lib/services/matching-service'

export function useMatches(filters?: {
  min_score?: number
  max_score?: number
  quality?: string
  include_dismissed?: boolean
  limit?: number
}) {
  const [data, setData] = useState<GrantMatch[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true

    async function fetchMatches() {
      try {
        setLoading(true)
        setError(null)
        const result = await matchingService.getMatches(filters)
        if (mounted) {
          setData(result)
        }
      } catch (err: any) {
        if (mounted) {
          setError(err.message || 'Failed to fetch matches')
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    fetchMatches()

    return () => {
      mounted = false
    }
  }, [JSON.stringify(filters)])

  return { data, loading, error }
}

export function useTopMatches(limit: number = 10) {
  const [data, setData] = useState<GrantMatch[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true

    async function fetchTopMatches() {
      try {
        setLoading(true)
        setError(null)
        const result = await matchingService.getTopMatches(limit)
        if (mounted) {
          setData(result)
        }
      } catch (err: any) {
        if (mounted) {
          setError(err.message || 'Failed to fetch top matches')
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    fetchTopMatches()

    return () => {
      mounted = false
    }
  }, [limit])

  return { data, loading, error }
}

export function useMatchStats() {
  const [data, setData] = useState<MatchStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true

    async function fetchStats() {
      try {
        setLoading(true)
        setError(null)
        const result = await matchingService.getMatchStats()
        if (mounted) {
          setData(result)
        }
      } catch (err: any) {
        if (mounted) {
          setError(err.message || 'Failed to fetch match stats')
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

// Made with Bob