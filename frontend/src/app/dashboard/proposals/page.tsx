'use client'

import { useState } from 'react'
import { TiptapEditor } from '@/components/proposals/tiptap-editor'
import { AISuggestions } from '@/components/proposals/ai-suggestions'
import { useProposalStore } from '@/lib/stores/proposal-store'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { motion } from 'framer-motion'

export default function ProposalsPage() {
  const { title, setTitle } = useProposalStore()
  const [isEditingTitle, setIsEditingTitle] = useState(false)

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6"
      >
        <div className="flex items-center justify-between mb-2">
          {isEditingTitle ? (
            <Input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              onBlur={() => setIsEditingTitle(false)}
              onKeyDown={(e) => e.key === 'Enter' && setIsEditingTitle(false)}
              className="text-3xl font-bold border-none shadow-none p-0 h-auto focus-visible:ring-0"
              autoFocus
            />
          ) : (
            <h1
              className="text-3xl font-bold text-gray-900 dark:text-gray-100 cursor-pointer hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
              onClick={() => setIsEditingTitle(true)}
            >
              {title}
            </h1>
          )}

          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <svg
                className="w-4 h-4 mr-1.5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"
                />
              </svg>
              Export
            </Button>
            <Button size="sm">
              <svg
                className="w-4 h-4 mr-1.5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"
                />
              </svg>
              Submit
            </Button>
          </div>
        </div>
        <p className="text-gray-600 dark:text-gray-400">
          Use AI tools to enhance your proposal writing
        </p>
      </motion.div>

      {/* Main Content */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 overflow-hidden">
        {/* Editor - Takes 2 columns on large screens */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="lg:col-span-2 border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden shadow-sm relative"
        >
          <TiptapEditor />
        </motion.div>

        {/* AI Suggestions Sidebar */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="overflow-y-auto"
        >
          <AISuggestions />
        </motion.div>
      </div>
    </div>
  )
}

// Made with Bob
