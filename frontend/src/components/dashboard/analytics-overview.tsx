'use client'

import { motion } from 'framer-motion'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

// Mock data for analytics
const applicationTrendData = [
  { month: 'Jan', applications: 12, approved: 8, rejected: 3, pending: 1 },
  { month: 'Feb', applications: 15, approved: 10, rejected: 4, pending: 1 },
  { month: 'Mar', applications: 18, approved: 12, rejected: 5, pending: 1 },
  { month: 'Apr', applications: 22, approved: 15, rejected: 6, pending: 1 },
  { month: 'May', applications: 28, approved: 19, rejected: 7, pending: 2 },
  { month: 'Jun', applications: 25, approved: 17, rejected: 6, pending: 2 },
]

const grantCategoryData = [
  { name: 'Research', value: 35, color: '#3b82f6' },
  { name: 'Education', value: 25, color: '#10b981' },
  { name: 'Healthcare', value: 20, color: '#f59e0b' },
  { name: 'Technology', value: 15, color: '#8b5cf6' },
  { name: 'Other', value: 5, color: '#6b7280' },
]

const successRateData = [
  { category: 'Research', rate: 75 },
  { category: 'Education', rate: 68 },
  { category: 'Healthcare', rate: 82 },
  { category: 'Technology', rate: 71 },
  { category: 'Arts', rate: 65 },
]

const fundingAmountData = [
  { month: 'Jan', amount: 125000 },
  { month: 'Feb', amount: 180000 },
  { month: 'Mar', amount: 220000 },
  { month: 'Apr', amount: 195000 },
  { month: 'May', amount: 280000 },
  { month: 'Jun', amount: 310000 },
]

interface AnalyticsOverviewProps {
  className?: string
}

export function AnalyticsOverview({ className = '' }: AnalyticsOverviewProps) {
  return (
    <div className={`space-y-6 ${className}`}>
      {/* Application Trends */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
          Application Trends
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={applicationTrendData}>
            <defs>
              <linearGradient id="colorApplications" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="month"
              stroke="#6b7280"
              style={{ fontSize: '12px' }}
            />
            <YAxis stroke="#6b7280" style={{ fontSize: '12px' }} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#fff',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
              }}
            />
            <Legend />
            <Area
              type="monotone"
              dataKey="applications"
              stroke="#3b82f6"
              fillOpacity={1}
              fill="url(#colorApplications)"
              strokeWidth={2}
            />
            <Line
              type="monotone"
              dataKey="approved"
              stroke="#10b981"
              strokeWidth={2}
              dot={{ r: 4 }}
            />
            <Line
              type="monotone"
              dataKey="rejected"
              stroke="#ef4444"
              strokeWidth={2}
              dot={{ r: 4 }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Grant Categories Distribution */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Grant Categories
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={grantCategoryData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) =>
                  `${name} ${((percent ?? 0) * 100).toFixed(0)}%`
                }
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {grantCategoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Success Rate by Category */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Success Rate by Category
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={successRateData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis
                dataKey="category"
                stroke="#6b7280"
                style={{ fontSize: '12px' }}
              />
              <YAxis
                stroke="#6b7280"
                style={{ fontSize: '12px' }}
                domain={[0, 100]}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                }}
                formatter={(value) => `${value}%`}
              />
              <Bar dataKey="rate" fill="#10b981" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Funding Amount Trends */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
          Funding Amount Trends
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={fundingAmountData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis
              dataKey="month"
              stroke="#6b7280"
              style={{ fontSize: '12px' }}
            />
            <YAxis
              stroke="#6b7280"
              style={{ fontSize: '12px' }}
              tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#fff',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
              }}
              formatter={(value) =>
                `$${Number(value).toLocaleString()}`
              }
            />
            <Line
              type="monotone"
              dataKey="amount"
              stroke="#8b5cf6"
              strokeWidth={3}
              dot={{ r: 5, fill: '#8b5cf6' }}
              activeDot={{ r: 7 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </motion.div>
    </div>
  )
}

// Made with Bob