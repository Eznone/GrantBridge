export type ProposalStatus = 'draft' | 'review' | 'submitted'

export interface Proposal {
  id: string
  grantId: string
  organizationId: string
  title: string
  content: string
  status: ProposalStatus
  aiGenerated: boolean
  createdAt: string
  updatedAt: string
}

export interface ProposalGenerationParams {
  grantId: string
  organizationId: string
  tone?: 'professional' | 'persuasive' | 'concise'
}

export interface ProposalUpdateData {
  title?: string
  content?: string
  status?: ProposalStatus
}

export interface AIImprovementParams {
  text: string
  action: 'rewrite' | 'expand' | 'shorten' | 'improve'
  tone?: 'professional' | 'persuasive' | 'concise'
}

// Made with Bob
