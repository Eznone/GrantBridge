export type GrantStatus = 'opportunity' | 'reviewing' | 'drafting' | 'submitted'

export interface Grant {
  id: string
  title: string
  fundingAmount: number
  requirements: string
  deadline: string
  tags: string[]
  source: string
  matchScore?: number
  status: GrantStatus
  description?: string
  eligibility?: string[]
  createdAt: string
  updatedAt?: string
}

export interface GrantFilters {
  search?: string
  minAmount?: number
  maxAmount?: number
  tags?: string[]
  status?: GrantStatus
  sortBy?: 'matchScore' | 'deadline' | 'fundingAmount'
  sortOrder?: 'asc' | 'desc'
}

export interface GrantUpdateData {
  status?: GrantStatus
  matchScore?: number
}

// Made with Bob
