'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

interface Grant {
  id: number
  title: string
  organization: string
  amount: string
  deadline: string
  category: string
  matchScore: number
  status: 'new' | 'saved' | 'applied'
  description: string
}

const mockGrants: Grant[] = [
  {
    id: 1,
    title: 'Community Development Grant 2024',
    organization: 'National Community Foundation',
    amount: '$50,000',
    deadline: '2024-03-15',
    category: 'Community Development',
    matchScore: 94,
    status: 'new',
    description: 'Supporting community-led initiatives that promote sustainable development and social cohesion.',
  },
  {
    id: 2,
    title: 'Education Innovation Fund',
    organization: 'Education Forward Initiative',
    amount: '$75,000',
    deadline: '2024-04-01',
    category: 'Education',
    matchScore: 89,
    status: 'saved',
    description: 'Funding innovative educational programs that improve student outcomes and teacher effectiveness.',
  },
  {
    id: 3,
    title: 'Environmental Sustainability Program',
    organization: 'Green Future Foundation',
    amount: '$100,000',
    deadline: '2024-04-20',
    category: 'Environment',
    matchScore: 85,
    status: 'new',
    description: 'Supporting projects that address climate change and promote environmental conservation.',
  },
  {
    id: 4,
    title: 'Healthcare Access Initiative',
    organization: 'Health for All Coalition',
    amount: '$60,000',
    deadline: '2024-03-30',
    category: 'Healthcare',
    matchScore: 82,
    status: 'applied',
    description: 'Improving healthcare access for underserved communities through innovative delivery models.',
  },
  {
    id: 5,
    title: 'Youth Empowerment Grant',
    organization: 'Youth Development Network',
    amount: '$45,000',
    deadline: '2024-05-15',
    category: 'Youth Development',
    matchScore: 78,
    status: 'new',
    description: 'Empowering young people through mentorship, skills training, and leadership development.',
  },
  {
    id: 6,
    title: 'Arts & Culture Preservation',
    organization: 'Cultural Heritage Trust',
    amount: '$55,000',
    deadline: '2024-04-10',
    category: 'Arts & Culture',
    matchScore: 75,
    status: 'saved',
    description: 'Preserving and promoting local arts and cultural traditions through community engagement.',
  },
]

const categories = ['All', 'Community Development', 'Education', 'Environment', 'Healthcare', 'Youth Development', 'Arts & Culture']
const statusFilters = ['All', 'New', 'Saved', 'Applied']

export default function GrantsPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [selectedStatus, setSelectedStatus] = useState('All')

  const filteredGrants = mockGrants.filter((grant) => {
    const matchesSearch = grant.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      grant.organization.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = selectedCategory === 'All' || grant.category === selectedCategory
    const matchesStatus = selectedStatus === 'All' || grant.status === selectedStatus.toLowerCase()
    return matchesSearch && matchesCategory && matchesStatus
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'new':
        return 'bg-blue-100 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400'
      case 'saved':
        return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/20 dark:text-yellow-400'
      case 'applied':
        return 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400'
      default:
        return 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
          Grant Opportunities
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Discover and track grant opportunities matched to your organization
        </p>
      </motion.div>

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6"
      >
        <div className="space-y-4">
          {/* Search */}
          <div className="relative">
            <svg
              className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
            <Input
              placeholder="Search grants by title or organization..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>

          {/* Category Filter */}
          <div>
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
              Category
            </label>
            <div className="flex flex-wrap gap-2">
              {categories.map((category) => (
                <Button
                  key={category}
                  variant={selectedCategory === category ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedCategory(category)}
                >
                  {category}
                </Button>
              ))}
            </div>
          </div>

          {/* Status Filter */}
          <div>
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
              Status
            </label>
            <div className="flex flex-wrap gap-2">
              {statusFilters.map((status) => (
                <Button
                  key={status}
                  variant={selectedStatus === status ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedStatus(status)}
                >
                  {status}
                </Button>
              ))}
            </div>
          </div>
        </div>
      </motion.div>

      {/* Results Count */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Showing {filteredGrants.length} of {mockGrants.length} grants
        </p>
        <Button variant="outline" size="sm">
          <svg
            className="w-4 h-4 mr-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12"
            />
          </svg>
          Sort by Match Score
        </Button>
      </div>

      {/* Grants Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredGrants.map((grant, index) => (
          <motion.div
            key={grant.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 + index * 0.05 }}
          >
            <Card className="hover:shadow-lg transition-shadow h-full">
              <CardHeader>
                <div className="flex items-start justify-between mb-2">
                  <div className="flex-1">
                    <CardTitle className="text-lg mb-1">{grant.title}</CardTitle>
                    <CardDescription>{grant.organization}</CardDescription>
                  </div>
                  <div className="flex items-center gap-1 px-2 py-1 bg-green-50 dark:bg-green-900/20 rounded-full">
                    <div className="w-2 h-2 rounded-full bg-green-500"></div>
                    <span className="text-xs font-semibold text-green-700 dark:text-green-400">
                      {grant.matchScore}%
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">{grant.category}</Badge>
                  <Badge className={getStatusColor(grant.status)}>
                    {grant.status.charAt(0).toUpperCase() + grant.status.slice(1)}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                  {grant.description}
                </p>
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <p className="text-xs text-gray-500 dark:text-gray-500">Amount</p>
                    <p className="text-lg font-bold text-gray-900 dark:text-gray-100">
                      {grant.amount}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-gray-500 dark:text-gray-500">Deadline</p>
                    <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                      {new Date(grant.deadline).toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric',
                      })}
                    </p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button className="flex-1" size="sm">
                    View Details
                  </Button>
                  {grant.status === 'new' && (
                    <Button variant="outline" size="sm">
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
                        />
                      </svg>
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

// Made with Bob
