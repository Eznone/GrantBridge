'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

interface Application {
  id: number
  grantTitle: string
  organization: string
  amount: string
  submittedDate: string
  status: 'draft' | 'submitted' | 'under_review' | 'approved' | 'rejected'
  deadline: string
  progress: number
}

const mockApplications: Application[] = [
  {
    id: 1,
    grantTitle: 'Community Development Grant 2024',
    organization: 'National Community Foundation',
    amount: '$50,000',
    submittedDate: '2024-02-15',
    status: 'under_review',
    deadline: '2024-03-15',
    progress: 100,
  },
  {
    id: 2,
    grantTitle: 'Education Innovation Fund',
    organization: 'Education Forward Initiative',
    amount: '$75,000',
    submittedDate: '2024-02-20',
    status: 'submitted',
    deadline: '2024-04-01',
    progress: 100,
  },
  {
    id: 3,
    grantTitle: 'Healthcare Access Initiative',
    organization: 'Health for All Coalition',
    amount: '$60,000',
    submittedDate: '2024-01-10',
    status: 'approved',
    deadline: '2024-03-30',
    progress: 100,
  },
  {
    id: 4,
    grantTitle: 'Youth Empowerment Grant',
    organization: 'Youth Development Network',
    amount: '$45,000',
    submittedDate: '',
    status: 'draft',
    deadline: '2024-05-15',
    progress: 65,
  },
  {
    id: 5,
    grantTitle: 'Environmental Sustainability Program',
    organization: 'Green Future Foundation',
    amount: '$100,000',
    submittedDate: '2024-01-05',
    status: 'rejected',
    deadline: '2024-04-20',
    progress: 100,
  },
]

const statusConfig = {
  draft: {
    label: 'Draft',
    color: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400',
    icon: '📝',
  },
  submitted: {
    label: 'Submitted',
    color: 'bg-blue-100 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400',
    icon: '📤',
  },
  under_review: {
    label: 'Under Review',
    color: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/20 dark:text-yellow-400',
    icon: '🔍',
  },
  approved: {
    label: 'Approved',
    color: 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400',
    icon: '✅',
  },
  rejected: {
    label: 'Rejected',
    color: 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400',
    icon: '❌',
  },
}

export default function ApplicationsPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('all')

  const filteredApplications = mockApplications.filter((app) => {
    const matchesSearch = app.grantTitle.toLowerCase().includes(searchQuery.toLowerCase()) ||
      app.organization.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = statusFilter === 'all' || app.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const stats = {
    total: mockApplications.length,
    draft: mockApplications.filter(a => a.status === 'draft').length,
    submitted: mockApplications.filter(a => a.status === 'submitted').length,
    under_review: mockApplications.filter(a => a.status === 'under_review').length,
    approved: mockApplications.filter(a => a.status === 'approved').length,
    rejected: mockApplications.filter(a => a.status === 'rejected').length,
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
          My Applications
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Track and manage your grant applications
        </p>
      </motion.div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {Object.entries(stats).map(([key, value], index) => (
          <motion.div
            key={key}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
          >
            <Card className="hover:shadow-md transition-shadow cursor-pointer" onClick={() => setStatusFilter(key === 'total' ? 'all' : key)}>
              <CardContent className="pt-6">
                <div className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-1">
                  {value}
                </div>
                <div className="text-xs text-gray-600 dark:text-gray-400 capitalize">
                  {key.replace('_', ' ')}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
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
              placeholder="Search applications..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>

          {/* Status Filter */}
          <div>
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
              Filter by Status
            </label>
            <div className="flex flex-wrap gap-2">
              <Button
                variant={statusFilter === 'all' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setStatusFilter('all')}
              >
                All
              </Button>
              {Object.entries(statusConfig).map(([key, config]) => (
                <Button
                  key={key}
                  variant={statusFilter === key ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setStatusFilter(key)}
                >
                  {config.icon} {config.label}
                </Button>
              ))}
            </div>
          </div>
        </div>
      </motion.div>

      {/* Applications List */}
      <div className="space-y-4">
        {filteredApplications.map((app, index) => {
          const config = statusConfig[app.status]
          return (
            <motion.div
              key={app.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 + index * 0.05 }}
            >
              <Card className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <CardTitle className="text-lg">{app.grantTitle}</CardTitle>
                        <Badge className={config.color}>
                          {config.icon} {config.label}
                        </Badge>
                      </div>
                      <CardDescription>{app.organization}</CardDescription>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                        {app.amount}
                      </p>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div>
                      <p className="text-xs text-gray-500 dark:text-gray-500 mb-1">
                        Deadline
                      </p>
                      <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                        {new Date(app.deadline).toLocaleDateString('en-US', {
                          month: 'short',
                          day: 'numeric',
                          year: 'numeric',
                        })}
                      </p>
                    </div>
                    {app.submittedDate && (
                      <div>
                        <p className="text-xs text-gray-500 dark:text-gray-500 mb-1">
                          Submitted
                        </p>
                        <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {new Date(app.submittedDate).toLocaleDateString('en-US', {
                            month: 'short',
                            day: 'numeric',
                            year: 'numeric',
                          })}
                        </p>
                      </div>
                    )}
                    <div>
                      <p className="text-xs text-gray-500 dark:text-gray-500 mb-1">
                        Progress
                      </p>
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                          <div
                            className="bg-gradient-to-r from-primary-500 to-accent-500 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${app.progress}%` }}
                          />
                        </div>
                        <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {app.progress}%
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    {app.status === 'draft' ? (
                      <>
                        <Button className="flex-1" size="sm">
                          Continue Editing
                        </Button>
                        <Button variant="outline" size="sm">
                          Delete
                        </Button>
                      </>
                    ) : (
                      <>
                        <Button className="flex-1" size="sm">
                          View Details
                        </Button>
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
                              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                            />
                          </svg>
                        </Button>
                      </>
                    )}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )
        })}
      </div>
    </div>
  )
}

// Made with Bob
