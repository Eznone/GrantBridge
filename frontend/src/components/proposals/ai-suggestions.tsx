'use client'

import { useProposalStore } from '@/lib/stores/proposal-store'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { motion, AnimatePresence } from 'framer-motion'

const actionLabels = {
  improve: 'Improved Writing',
  expand: 'Expanded Text',
  summarize: 'Summarized',
  tone: 'Tone Adjusted',
}

const actionIcons = {
  improve: '✨',
  expand: '📝',
  summarize: '📋',
  tone: '🎨',
}

export function AISuggestions() {
  const { aiSuggestions, applySuggestion, dismissSuggestion, clearSuggestions } =
    useProposalStore()

  if (aiSuggestions.length === 0) {
    return null
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 flex items-center gap-2">
          <span className="text-2xl">🤖</span>
          AI Suggestions ({aiSuggestions.length})
        </h3>
        {aiSuggestions.length > 0 && (
          <Button variant="ghost" size="sm" onClick={clearSuggestions}>
            Clear All
          </Button>
        )}
      </div>

      <AnimatePresence mode="popLayout">
        {aiSuggestions.map((suggestion) => (
          <motion.div
            key={suggestion.id}
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, x: -100, scale: 0.95 }}
            transition={{ duration: 0.2 }}
          >
            <Card
              className={`p-4 ${
                suggestion.applied
                  ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
                  : 'bg-white dark:bg-gray-800'
              }`}
            >
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center text-lg">
                  {actionIcons[suggestion.type]}
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                      {actionLabels[suggestion.type]}
                    </span>
                    {suggestion.applied && (
                      <span className="text-xs px-2 py-0.5 rounded-full bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 font-medium">
                        Applied
                      </span>
                    )}
                  </div>

                  <div className="space-y-3">
                    <div>
                      <p className="text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">
                        Original:
                      </p>
                      <p className="text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-900/50 p-2 rounded">
                        {suggestion.original}
                      </p>
                    </div>

                    <div>
                      <p className="text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">
                        Suggestion:
                      </p>
                      <p className="text-sm text-gray-900 dark:text-gray-100 bg-primary-50 dark:bg-primary-900/20 p-2 rounded border border-primary-200 dark:border-primary-800">
                        {suggestion.suggestion}
                      </p>
                    </div>
                  </div>

                  {!suggestion.applied && (
                    <div className="flex items-center gap-2 mt-3">
                      <Button
                        size="sm"
                        onClick={() => applySuggestion(suggestion.id)}
                        className="gap-1.5"
                      >
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
                            d="M5 13l4 4L19 7"
                          />
                        </svg>
                        Apply
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => dismissSuggestion(suggestion.id)}
                      >
                        Dismiss
                      </Button>
                    </div>
                  )}
                </div>
              </div>
            </Card>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  )
}

// Made with Bob