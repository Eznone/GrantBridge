'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/stores/auth-store'

export default function HomePage() {
  const router = useRouter()
  const { isAuthenticated, _hasHydrated } = useAuthStore()

  useEffect(() => {
    if (_hasHydrated) {
      if (isAuthenticated) {
        router.replace('/dashboard')
      } else {
        router.replace('/login')
      }
    }
  }, [isAuthenticated, _hasHydrated, router])

  // Show loading state while determining auth status
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-accent-50 dark:from-gray-900 dark:to-gray-800">
      <div className="text-center space-y-6 p-8">
        <div className="w-16 h-16 mx-auto bg-gradient-to-br from-primary-500 to-accent-500 rounded-2xl flex items-center justify-center shadow-lg animate-pulse">
          <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <h1 className="text-5xl font-bold bg-gradient-to-r from-primary-600 to-accent-600 bg-clip-text text-transparent">
          GrantBridge
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl">
          AI-Powered Grant Assistant for NGOs
        </p>
        <div className="flex items-center justify-center gap-2 text-gray-500 dark:text-gray-400">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
          <span>Loading...</span>
        </div>
      </div>
    </div>
  )
}

// Made with Bob
