'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { ErrorState } from '@/components/ui/error-state'
import { useGrants } from '@/lib/hooks/use-grants'
import { GrantFilters } from '@/lib/services/grant-service'

const categories = ['All', 'Community Development', 'Education', 'Environment', 'Healthcare', 'Youth Development', 'Arts & Culture']

export default function GrantsPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [sortBy, setSortBy] = useState('deadline')

  // Build filters for API
  const filters: GrantFilters = {
    search: searchQuery || undefined,
    categories: selectedCategory !== 'All' ? selectedCategory : undefined,
    sort_by: sortBy,
    page: 1,
    page_size: 20,
  }

  // Fetch grants from backend
  const { data: grantsData, loading, error } = useGrants(filters)

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

        </div>
      </motion.div>

      {/* Results Count */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-600 dark:text-gray-400">
          {loading ? 'Loading...' : `Showing ${grantsData?.grants.length || 0} of ${grantsData?.total || 0} grants`}
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
          Sort by {sortBy === 'deadline' ? 'Deadline' : 'Match Score'}
        </Button>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="flex items-center justify-center py-12">
          <LoadingSpinner size="lg" />
        </div>
      )}

      {/* Error State */}
      {error && <ErrorState message={error} />}

      {/* Grants Grid */}
      {!loading && !error && grantsData && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {grantsData.grants.length === 0 ? (
            <div className="col-span-2 text-center py-12">
              <p className="text-gray-500">No grants found matching your criteria</p>
            </div>
          ) : (
            grantsData.grants.map((grant, index) => (
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
                        <CardDescription>{grant.source}</CardDescription>
                      </div>
                      <div className="flex items-center gap-1 px-2 py-1 bg-green-50 dark:bg-green-900/20 rounded-full">
                        <div className="w-2 h-2 rounded-full bg-green-500"></div>
                        <span className="text-xs font-semibold text-green-700 dark:text-green-400">
                          AI Match
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      {grant.tags && grant.tags.length > 0 && (
                        <Badge variant="secondary">{grant.tags[0]}</Badge>
                      )}
                      <Badge className={getStatusColor('new')}>
                        Available
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                      {grant.description?.substring(0, 150)}...
                    </p>
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <p className="text-xs text-gray-500 dark:text-gray-500">Amount</p>
                        <p className="text-lg font-bold text-gray-900 dark:text-gray-100">
                          ${grant.fundingAmount?.toLocaleString() || 'N/A'}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="text-xs text-gray-500 dark:text-gray-500">Deadline</p>
                        <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {grant.deadline ? new Date(grant.deadline).toLocaleDateString('en-US', {
                            month: 'short',
                            day: 'numeric',
                            year: 'numeric',
                          }) : 'N/A'}
                        </p>
                      </div>
                    </div>
                    <div className="flex gap-2">
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
                            d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
                          />
                        </svg>
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))
          )}
        </div>
      )}
    </div>
  )
}

// Made with Bob
