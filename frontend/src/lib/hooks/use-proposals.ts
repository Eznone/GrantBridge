/**
 * Custom hooks for proposal data fetching
 */

import { useState, useEffect } from 'react'
import { proposalService, ProposalFilters } from '@/lib/services/proposal-service'
import { Proposal } from '@/types/proposal'

export function useProposals(filters?: ProposalFilters) {
  const [data, setData] = useState<Proposal[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true

    async function fetchProposals() {
      try {
        setLoading(true)
        setError(null)
        const result = await proposalService.listProposals(filters)
        if (mounted) {
          setData(result)
        }
      } catch (err: any) {
        if (mounted) {
          setError(err.message || 'Failed to fetch proposals')
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    fetchProposals()

    return () => {
      mounted = false
    }
  }, [JSON.stringify(filters)])

  return { data, loading, error }
}

export function useProposal(id: string | null) {
  const [data, setData] = useState<Proposal | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) {
      setLoading(false)
      return
    }

    let mounted = true

    async function fetchProposal() {
      try {
        setLoading(true)
        setError(null)
        const result = await proposalService.getProposal(id!)
        if (mounted) {
          setData(result)
        }
      } catch (err: any) {
        if (mounted) {
          setError(err.message || 'Failed to fetch proposal')
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    fetchProposal()

    return () => {
      mounted = false
    }
  }, [id])

  return { data, loading, error }
}

// Made with Bob