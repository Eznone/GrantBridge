'use client'

import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'
import { useEffect, useState } from 'react'
import { useProposalStore, type AIAction, type AITone } from '@/lib/stores/proposal-store'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils/cn'

const tones: { value: AITone; label: string; icon: string }[] = [
  { value: 'professional', label: 'Professional', icon: '💼' },
  { value: 'friendly', label: 'Friendly', icon: '😊' },
  { value: 'formal', label: 'Formal', icon: '🎩' },
  { value: 'persuasive', label: 'Persuasive', icon: '🎯' },
]

const aiActions: { value: AIAction; label: string; icon: string }[] = [
  { value: 'improve', label: 'Improve Writing', icon: '✨' },
  { value: 'expand', label: 'Expand', icon: '📝' },
  { value: 'summarize', label: 'Summarize', icon: '📋' },
  { value: 'tone', label: 'Adjust Tone', icon: '🎨' },
]

export function TiptapEditor() {
  const {
    content,
    setContent,
    generateAISuggestion,
    isAILoading,
    selectedTone,
    setSelectedTone,
    autoSaveStatus,
  } = useProposalStore()

  const [selectedText, setSelectedText] = useState('')
  const [showToneSelector, setShowToneSelector] = useState(false)

  const editor = useEditor({
    extensions: [
      StarterKit,
      Placeholder.configure({
        placeholder: 'Start writing your proposal here...',
      }),
    ],
    content,
    onUpdate: ({ editor }) => {
      setContent(editor.getHTML())
    },
    onSelectionUpdate: ({ editor }) => {
      const { from, to } = editor.state.selection
      const text = editor.state.doc.textBetween(from, to, ' ')
      setSelectedText(text)
    },
    editorProps: {
      attributes: {
        class:
          'prose prose-sm sm:prose lg:prose-lg xl:prose-xl focus:outline-none min-h-[500px] max-w-none p-6',
      },
    },
  })

  useEffect(() => {
    if (editor && content !== editor.getHTML()) {
      editor.commands.setContent(content)
    }
  }, [content, editor])

  const handleAIAction = async (action: AIAction) => {
    if (!selectedText.trim()) {
      alert('Please select some text first')
      return
    }
    await generateAISuggestion(action, selectedText)
  }

  return (
    <div className="flex flex-col h-full">
      {/* AI Toolbar */}
      <div className="border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-3 flex items-center gap-2 flex-wrap">
        <div className="flex items-center gap-2 mr-4">
          <span className="text-xs font-medium text-gray-500 dark:text-gray-400">AI Tools:</span>
        </div>

        {aiActions.map((action) => (
          <Button
            key={action.value}
            variant="outline"
            size="sm"
            onClick={() => handleAIAction(action.value)}
            disabled={isAILoading || !selectedText}
            className="gap-1.5"
          >
            <span>{action.icon}</span>
            <span className="hidden sm:inline">{action.label}</span>
          </Button>
        ))}

        <div className="relative ml-auto">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowToneSelector(!showToneSelector)}
            className="gap-1.5"
          >
            <span>🎨</span>
            <span className="hidden sm:inline">Tone: {selectedTone}</span>
          </Button>

          {showToneSelector && (
            <>
              <div
                className="fixed inset-0 z-40"
                onClick={() => setShowToneSelector(false)}
              />
              <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-1 z-50">
                {tones.map((tone) => (
                  <button
                    key={tone.value}
                    onClick={() => {
                      setSelectedTone(tone.value)
                      setShowToneSelector(false)
                    }}
                    className={cn(
                      'w-full px-4 py-2 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2',
                      selectedTone === tone.value && 'bg-primary-50 dark:bg-primary-900/20'
                    )}
                  >
                    <span>{tone.icon}</span>
                    <span>{tone.label}</span>
                  </button>
                ))}
              </div>
            </>
          )}
        </div>

        {/* Auto-save indicator */}
        <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 ml-4">
          {autoSaveStatus === 'saving' && (
            <>
              <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-primary-600"></div>
              <span>Saving...</span>
            </>
          )}
          {autoSaveStatus === 'saved' && (
            <>
              <svg className="w-3 h-3 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
              <span>Saved</span>
            </>
          )}
          {autoSaveStatus === 'unsaved' && <span>Unsaved changes</span>}
        </div>
      </div>

      {/* Editor */}
      <div className="flex-1 overflow-y-auto bg-white dark:bg-gray-900">
        <EditorContent editor={editor} />
      </div>

      {/* AI Loading Overlay */}
      {isAILoading && (
        <div className="absolute inset-0 bg-black/20 dark:bg-black/40 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-xl flex flex-col items-center gap-3">
            <div className="relative">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-2xl">✨</span>
              </div>
            </div>
            <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
              AI is analyzing your text...
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

// Made with Bob