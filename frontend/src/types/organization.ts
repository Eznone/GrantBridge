export interface Organization {
  id: string
  name: string
  mission: string
  goals: string[]
  categories: string[]
  historicalProjects: string[]
  fundingNeeds: number
  createdAt: string
  updatedAt: string
}

export interface OrganizationUpdateData {
  name?: string
  mission?: string
  goals?: string[]
  categories?: string[]
  historicalProjects?: string[]
  fundingNeeds?: number
}

// Made with Bob
