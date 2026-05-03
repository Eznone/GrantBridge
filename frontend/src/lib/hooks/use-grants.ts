/**
 * Custom hooks for grant data fetching
 */

import { useState, useEffect } from 'react'
import { grantService, GrantFilters, GrantListResponse } from '@/lib/services/grant-service'
import { Grant } from '@/types/grant'

export function useGrants(filters?: GrantFilters) {
  const [data, setData] = useState<GrantListResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true

    async function fetchGrants() {
      try {
        setLoading(true)
        setError(null)
        const result = await grantService.listGrants(filters)
        if (mounted) {
          setData(result)
        }
      } catch (err: any) {
        if (mounted) {
          setError(err.message || 'Failed to fetch grants')
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    fetchGrants()

    return () => {
      mounted = false
    }
  }, [JSON.stringify(filters)])

  return { data, loading, error, refetch: () => {} }
}

export function useGrant(id: string | null) {
  const [data, setData] = useState<Grant | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) {
      setLoading(false)
      return
    }

    let mounted = true

    async function fetchGrant() {
      try {
        setLoading(true)
        setError(null)
        const result = await grantService.getGrant(id!)
        if (mounted) {
          setData(result)
        }
      } catch (err: any) {
        if (mounted) {
          setError(err.message || 'Failed to fetch grant')
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    fetchGrant()

    return () => {
      mounted = false
    }
  }, [id])

  return { data, loading, error }
}

export function useSavedGrants() {
  const [data, setData] = useState<Grant[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true

    async function fetchSavedGrants() {
      try {
        setLoading(true)
        setError(null)
        const result = await grantService.getSavedGrants()
        if (mounted) {
          setData(result)
        }
      } catch (err: any) {
        if (mounted) {
          setError(err.message || 'Failed to fetch saved grants')
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    fetchSavedGrants()

    return () => {
      mounted = false
    }
  }, [])

  return { data, loading, error }
}

// Made with Bob