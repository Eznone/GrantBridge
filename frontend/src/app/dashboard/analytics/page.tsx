'use client'

import { motion } from 'framer-motion'
import { AnalyticsOverview } from '@/components/dashboard/analytics-overview'
import { StatCards } from '@/components/dashboard/stat-cards'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
          Analytics & Insights
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Track your grant application performance and success metrics
        </p>
      </motion.div>

      {/* Key Metrics */}
      <StatCards />

      {/* Detailed Analytics */}
      <AnalyticsOverview />

      {/* Additional Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Card>
            <CardHeader>
              <CardTitle>Top Performing Categories</CardTitle>
              <CardDescription>
                Categories with highest success rates
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { category: 'Healthcare', rate: 82, applications: 12 },
                  { category: 'Research', rate: 75, applications: 18 },
                  { category: 'Education', rate: 68, applications: 15 },
                  { category: 'Technology', rate: 71, applications: 9 },
                ].map((item, index) => (
                  <div key={item.category} className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="font-medium text-gray-900 dark:text-gray-100">
                        {item.category}
                      </span>
                      <span className="text-gray-600 dark:text-gray-400">
                        {item.rate}% ({item.applications} apps)
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-gradient-to-r from-primary-500 to-accent-500 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${item.rate}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>
                Latest updates on your applications
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  {
                    action: 'Application Approved',
                    grant: 'Healthcare Access Initiative',
                    time: '2 hours ago',
                    icon: '✅',
                    color: 'text-green-600 dark:text-green-400',
                  },
                  {
                    action: 'Proposal Submitted',
                    grant: 'Education Innovation Fund',
                    time: '1 day ago',
                    icon: '📤',
                    color: 'text-blue-600 dark:text-blue-400',
                  },
                  {
                    action: 'New Grant Match',
                    grant: 'Community Development Grant',
                    time: '2 days ago',
                    icon: '🎯',
                    color: 'text-purple-600 dark:text-purple-400',
                  },
                  {
                    action: 'Deadline Reminder',
                    grant: 'Youth Empowerment Grant',
                    time: '3 days ago',
                    icon: '⏰',
                    color: 'text-orange-600 dark:text-orange-400',
                  },
                ].map((activity, index) => (
                  <div
                    key={index}
                    className="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                  >
                    <div className={`text-2xl ${activity.color}`}>
                      {activity.icon}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                        {activity.action}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400 truncate">
                        {activity.grant}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                        {activity.time}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}

// Made with Bob