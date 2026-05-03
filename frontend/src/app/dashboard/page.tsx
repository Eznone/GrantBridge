'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { AnalyticsOverview } from '@/components/dashboard/analytics-overview'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import { ErrorState } from '@/components/ui/error-state'
import { useDashboardStats } from '@/lib/hooks/use-dashboard'
import { useTopMatches } from '@/lib/hooks/use-matching'
import { useProposals } from '@/lib/hooks/use-proposals'

const icons = {
  fileText: (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  ),
  dollarSign: (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
  target: (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
  fileCheck: (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
  trendingUp: (
    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
    </svg>
  ),
  sparkles: (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
    </svg>
  ),
}

export default function DashboardPage() {
  // Fetch data from backend
  const { data: stats, loading: statsLoading, error: statsError } = useDashboardStats()
  const { data: topMatches, loading: matchesLoading, error: matchesError } = useTopMatches(3)
  const { data: proposals, loading: proposalsLoading, error: proposalsError } = useProposals({
    status: 'draft,review',
    page_size: 3
  })

  // Show loading state
  if (statsLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  // Show error state
  if (statsError) {
    return <ErrorState message={statsError} />
  }

  // Prepare stats for display
  const displayStats = stats ? [
    {
      title: 'Active Applications',
      value: stats.active_applications.toString(),
      icon: icons.fileText,
      trend: '+12%',
      trendUp: true,
    },
    {
      title: 'Total Funding Sought',
      value: `$${stats.total_funding.toLocaleString()}`,
      icon: icons.dollarSign,
      trend: '+8%',
      trendUp: true,
    },
    {
      title: 'Match Rate',
      value: `${Math.round(stats.success_rate)}%`,
      icon: icons.target,
      trend: '+5%',
      trendUp: true,
    },
    {
      title: 'Proposals Drafted',
      value: stats.total_proposals.toString(),
      icon: icons.fileCheck,
      trend: '+18%',
      trendUp: true,
    },
  ] : []
  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Welcome back! Here's an overview of your grant applications and proposals.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {displayStats.map((stat, index) => (
          <Card key={index} className="hover:shadow-lg transition-shadow duration-200">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
                {stat.title}
              </CardTitle>
              <div className="text-gray-400 dark:text-gray-500">
                {stat.icon}
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-gray-900 dark:text-gray-100">{stat.value}</div>
              {stat.trend && (
                <p className="text-xs text-green-600 dark:text-green-400 mt-2 flex items-center gap-1">
                  {icons.trendingUp}
                  <span>{stat.trend} from last month</span>
                </p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* New Grant Opportunities */}
        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-xl">New Grant Opportunities</CardTitle>
                <CardDescription className="mt-1">
                  AI-matched grants for your organization
                </CardDescription>
              </div>
              <div className="flex items-center gap-1 px-2 py-1 bg-primary-50 dark:bg-primary-900/20 rounded-full">
                {icons.sparkles}
                <span className="text-xs font-medium text-primary-700 dark:text-primary-400">AI</span>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {matchesLoading ? (
                <LoadingSpinner />
              ) : matchesError ? (
                <p className="text-sm text-red-600">{matchesError}</p>
              ) : topMatches.length === 0 ? (
                <p className="text-sm text-gray-500">No matches found</p>
              ) : (
                topMatches.map((match) => (
                  <div
                    key={match.id}
                    className="p-4 rounded-lg border border-gray-200 dark:border-gray-800 hover:border-primary-300 dark:hover:border-primary-700 transition-colors cursor-pointer group"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-gray-900 dark:text-gray-100 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                        {match.grant_title}
                      </h3>
                      <div className="flex items-center gap-1 px-2 py-0.5 bg-green-50 dark:bg-green-900/20 rounded-full">
                        <div className="w-1.5 h-1.5 rounded-full bg-green-500"></div>
                        <span className="text-xs font-semibold text-green-700 dark:text-green-400">
                          {Math.round(match.match_score)}%
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
                      <span className="font-medium text-gray-900 dark:text-gray-100">{match.quality}</span>
                      <span>Match Quality</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>

        {/* Proposals in Progress */}
        <Card className="hover:shadow-lg transition-shadow duration-200">
          <CardHeader>
            <CardTitle className="text-xl">Proposals in Progress</CardTitle>
            <CardDescription className="mt-1">
              Continue working on your drafts
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {proposalsLoading ? (
                <LoadingSpinner />
              ) : proposalsError ? (
                <p className="text-sm text-red-600">{proposalsError}</p>
              ) : proposals.length === 0 ? (
                <p className="text-sm text-gray-500">No proposals in progress</p>
              ) : (
                proposals.map((proposal) => (
                  <div
                    key={proposal.id}
                    className="p-4 rounded-lg border border-gray-200 dark:border-gray-800 hover:border-primary-300 dark:hover:border-primary-700 transition-colors cursor-pointer"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="font-semibold text-gray-900 dark:text-gray-100">
                        {proposal.title}
                      </h3>
                      <span className="text-xs px-2 py-1 rounded-full bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 font-medium">
                        {proposal.status}
                      </span>
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-xs text-gray-600 dark:text-gray-400">
                        <span>Status</span>
                        <span className="font-medium capitalize">{proposal.status}</span>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card className="bg-gradient-to-br from-primary-50 to-accent-50 dark:from-primary-900/20 dark:to-accent-900/20 border-primary-100 dark:border-primary-800">
        <CardHeader>
          <CardTitle className="text-xl flex items-center gap-2">
            {icons.sparkles}
            <span>AI-Powered Quick Actions</span>
          </CardTitle>
          <CardDescription>
            Let AI help you with your grant applications
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <button className="p-4 rounded-lg bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 hover:border-primary-300 dark:hover:border-primary-700 transition-all hover:shadow-md text-left group">
              <div className="text-2xl mb-2">🎯</div>
              <h3 className="font-semibold text-gray-900 dark:text-gray-100 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                Find Matching Grants
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Discover grants that match your mission
              </p>
            </button>
            <button className="p-4 rounded-lg bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 hover:border-primary-300 dark:hover:border-primary-700 transition-all hover:shadow-md text-left group">
              <div className="text-2xl mb-2">✍️</div>
              <h3 className="font-semibold text-gray-900 dark:text-gray-100 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                Generate Proposal
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Create a draft with AI assistance
              </p>
            </button>
            <button className="p-4 rounded-lg bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 hover:border-primary-300 dark:hover:border-primary-700 transition-all hover:shadow-md text-left group">
              <div className="text-2xl mb-2">💡</div>
              <h3 className="font-semibold text-gray-900 dark:text-gray-100 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                Improve Writing
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Enhance your existing proposals
              </p>
            </button>
          </div>
        </CardContent>
      </Card>

      {/* Analytics Section */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">
          Analytics & Insights
        </h2>
        <AnalyticsOverview />
      </div>
    </div>
  )
}

// Made with Bob