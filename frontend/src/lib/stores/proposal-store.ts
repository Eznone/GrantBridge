'use client'

import { create } from 'zustand'

export type AITone = 'professional' | 'friendly' | 'formal' | 'persuasive'
export type AIAction = 'improve' | 'expand' | 'summarize' | 'tone'

interface AISuggestion {
  id: string
  type: AIAction
  original: string
  suggestion: string
  applied: boolean
}

interface ProposalState {
  content: string
  title: string
  isAILoading: boolean
  aiSuggestions: AISuggestion[]
  selectedTone: AITone
  autoSaveStatus: 'saved' | 'saving' | 'unsaved'
  lastSaved: Date | null

  setContent: (content: string) => void
  setTitle: (title: string) => void
  setSelectedTone: (tone: AITone) => void
  generateAISuggestion: (action: AIAction, selectedText: string) => Promise<void>
  applySuggestion: (suggestionId: string) => void
  dismissSuggestion: (suggestionId: string) => void
  clearSuggestions: () => void
  triggerAutoSave: () => void
}

// Mock AI responses
const mockAIResponses = {
  improve: (text: string) => {
    return text
      .replace(/\b(good|nice|great)\b/gi, 'excellent')
      .replace(/\b(help|assist)\b/gi, 'support')
      .replace(/\b(make|create)\b/gi, 'develop')
  },
  expand: (text: string) => {
    return `${text} Furthermore, this initiative will create lasting impact by fostering sustainable development and empowering communities through innovative solutions and collaborative partnerships.`
  },
  summarize: (text: string) => {
    const words = text.split(' ')
    return words.slice(0, Math.ceil(words.length / 2)).join(' ') + '...'
  },
  tone: {
    professional: (text: string) => text.replace(/!/g, '.').replace(/\?/g, '.'),
    friendly: (text: string) => text + ' We look forward to collaborating with you!',
    formal: (text: string) => 'Respectfully, ' + text,
    persuasive: (text: string) => text + ' This represents a unique opportunity for meaningful impact.',
  },
}

export const useProposalStore = create<ProposalState>((set, get) => ({
  content: '',
  title: 'Untitled Proposal',
  isAILoading: false,
  aiSuggestions: [],
  selectedTone: 'professional',
  autoSaveStatus: 'saved',
  lastSaved: null,

  setContent: (content) => {
    set({ content, autoSaveStatus: 'unsaved' })
    // Trigger auto-save after 2 seconds of inactivity
    setTimeout(() => {
      get().triggerAutoSave()
    }, 2000)
  },

  setTitle: (title) => {
    set({ title, autoSaveStatus: 'unsaved' })
  },

  setSelectedTone: (tone) => {
    set({ selectedTone: tone })
  },

  generateAISuggestion: async (action, selectedText) => {
    if (!selectedText.trim()) return

    set({ isAILoading: true })

    // Simulate AI processing delay
    await new Promise((resolve) => setTimeout(resolve, 1500))

    const suggestion: AISuggestion = {
      id: `suggestion-${Date.now()}`,
      type: action,
      original: selectedText,
      suggestion:
        action === 'tone'
          ? mockAIResponses.tone[get().selectedTone](selectedText)
          : mockAIResponses[action](selectedText),
      applied: false,
    }

    set((state) => ({
      aiSuggestions: [suggestion, ...state.aiSuggestions],
      isAILoading: false,
    }))
  },

  applySuggestion: (suggestionId) => {
    const suggestion = get().aiSuggestions.find((s) => s.id === suggestionId)
    if (!suggestion) return

    const content = get().content.replace(suggestion.original, suggestion.suggestion)
    set({
      content,
      aiSuggestions: get().aiSuggestions.map((s) =>
        s.id === suggestionId ? { ...s, applied: true } : s
      ),
      autoSaveStatus: 'unsaved',
    })
  },

  dismissSuggestion: (suggestionId) => {
    set({
      aiSuggestions: get().aiSuggestions.filter((s) => s.id !== suggestionId),
    })
  },

  clearSuggestions: () => {
    set({ aiSuggestions: [] })
  },

  triggerAutoSave: () => {
    set({ autoSaveStatus: 'saving' })
    // Simulate save delay
    setTimeout(() => {
      set({ autoSaveStatus: 'saved', lastSaved: new Date() })
    }, 500)
  },
}))

// Made with Bob