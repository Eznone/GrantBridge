'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'

interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface Conversation {
  id: number
  title: string
  lastMessage: string
  timestamp: Date
  messages: Message[]
}

const mockConversations: Conversation[] = [
  {
    id: 1,
    title: 'Grant Writing Tips',
    lastMessage: 'Here are some best practices for writing compelling grant proposals...',
    timestamp: new Date('2026-08-20T10:30:00'),
    messages: [
      {
        id: 1,
        role: 'user',
        content: 'Can you help me write a better grant proposal?',
        timestamp: new Date('2026-08-20T10:25:00'),
      },
      {
        id: 2,
        role: 'assistant',
        content: 'Here are some best practices for writing compelling grant proposals...',
        timestamp: new Date('2026-08-20T10:30:00'),
      },
    ],
  },
  {
    id: 2,
    title: 'Budget Planning',
    lastMessage: 'Let me help you create a detailed budget breakdown...',
    timestamp: new Date('2026-08-19T14:15:00'),
    messages: [
      {
        id: 1,
        role: 'user',
        content: 'How should I structure my grant budget?',
        timestamp: new Date('2026-08-19T14:10:00'),
      },
      {
        id: 2,
        role: 'assistant',
        content: 'Let me help you create a detailed budget breakdown...',
        timestamp: new Date('2026-08-19T14:15:00'),
      },
    ],
  },
]

const quickActions = [
  {
    icon: '✍️',
    title: 'Improve Writing',
    description: 'Enhance your proposal text',
    prompt: 'Help me improve this grant proposal section:',
  },
  {
    icon: '🎯',
    title: 'Find Grants',
    description: 'Discover matching opportunities',
    prompt: 'Find grants that match my organization profile',
  },
  {
    icon: '📊',
    title: 'Budget Help',
    description: 'Create budget breakdowns',
    prompt: 'Help me create a budget for a $50,000 grant',
  },
  {
    icon: '📝',
    title: 'Draft Proposal',
    description: 'Generate proposal sections',
    prompt: 'Help me draft a project description for',
  },
]

export default function AIAssistantPage() {
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null)
  const [inputMessage, setInputMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return
    
    setIsTyping(true)
    // Simulate AI response
    setTimeout(() => {
      setIsTyping(false)
      setInputMessage('')
    }, 2000)
  }

  const handleQuickAction = (prompt: string) => {
    setInputMessage(prompt + ' ')
  }

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6"
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
          AI Assistant
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Get help with grant writing, research, and strategy
        </p>
      </motion.div>

      {/* Main Content */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-6 overflow-hidden">
        {/* Conversations Sidebar */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="lg:col-span-1 space-y-4 overflow-y-auto"
        >
          <Button className="w-full" onClick={() => setSelectedConversation(null)}>
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
                d="M12 4v16m8-8H4"
              />
            </svg>
            New Conversation
          </Button>

          <div className="space-y-2">
            {mockConversations.map((conv) => (
              <Card
                key={conv.id}
                className={`cursor-pointer transition-all hover:shadow-md ${
                  selectedConversation?.id === conv.id
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                    : ''
                }`}
                onClick={() => setSelectedConversation(conv)}
              >
                <CardHeader className="p-4">
                  <CardTitle className="text-sm">{conv.title}</CardTitle>
                  <CardDescription className="text-xs line-clamp-2">
                    {conv.lastMessage}
                  </CardDescription>
                  <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
                    {conv.timestamp.toLocaleDateString()}
                  </p>
                </CardHeader>
              </Card>
            ))}
          </div>
        </motion.div>

        {/* Chat Area */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="lg:col-span-3 flex flex-col border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden"
        >
          {selectedConversation ? (
            <>
              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50 dark:bg-gray-900/50">
                {selectedConversation.messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${
                      message.role === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg p-4 ${
                        message.role === 'user'
                          ? 'bg-primary-600 text-white'
                          : 'bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 border border-gray-200 dark:border-gray-700'
                      }`}
                    >
                      <p className="text-sm">{message.content}</p>
                      <p
                        className={`text-xs mt-2 ${
                          message.role === 'user'
                            ? 'text-primary-100'
                            : 'text-gray-500 dark:text-gray-500'
                        }`}
                      >
                        {message.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))}
                {isTyping && (
                  <div className="flex justify-start">
                    <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
                      <div className="flex gap-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Input */}
              <div className="p-4 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
                <div className="flex gap-2">
                  <Textarea
                    placeholder="Ask me anything about grants..."
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault()
                        handleSendMessage()
                      }
                    }}
                    rows={2}
                    className="resize-none"
                  />
                  <Button onClick={handleSendMessage} disabled={!inputMessage.trim()}>
                    <svg
                      className="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                      />
                    </svg>
                  </Button>
                </div>
              </div>
            </>
          ) : (
            /* Welcome Screen */
            <div className="flex-1 flex flex-col items-center justify-center p-8 bg-gradient-to-br from-primary-50 to-accent-50 dark:from-primary-900/20 dark:to-accent-900/20">
              <div className="text-6xl mb-4">🤖</div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                AI Grant Assistant
              </h2>
              <p className="text-gray-600 dark:text-gray-400 text-center max-w-md mb-8">
                I can help you with grant writing, research, budgeting, and strategy.
                Choose a quick action or start a new conversation.
              </p>

              {/* Quick Actions */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-2xl">
                {quickActions.map((action, index) => (
                  <motion.div
                    key={action.title}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 + index * 0.1 }}
                  >
                    <Card
                      className="cursor-pointer hover:shadow-lg transition-all hover:border-primary-300 dark:hover:border-primary-700"
                      onClick={() => handleQuickAction(action.prompt)}
                    >
                      <CardHeader>
                        <div className="text-3xl mb-2">{action.icon}</div>
                        <CardTitle className="text-lg">{action.title}</CardTitle>
                        <CardDescription>{action.description}</CardDescription>
                      </CardHeader>
                    </Card>
                  </motion.div>
                ))}
              </div>

              {/* Input */}
              <div className="w-full max-w-2xl mt-8">
                <div className="flex gap-2">
                  <Input
                    placeholder="Ask me anything about grants..."
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') {
                        e.preventDefault()
                        handleSendMessage()
                      }
                    }}
                    className="flex-1"
                  />
                  <Button onClick={handleSendMessage} disabled={!inputMessage.trim()}>
                    <svg
                      className="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                      />
                    </svg>
                  </Button>
                </div>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
}

// Made with Bob
