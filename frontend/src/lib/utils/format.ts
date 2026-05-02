/**
 * Format a number as currency (USD)
 */
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount)
}

/**
 * Format a date string to a readable format
 */
export function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(date)
}

/**
 * Format a date string to a relative time (e.g., "2 days ago")
 */
export function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000)

  if (diffInSeconds < 60) return 'just now'
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`
  if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`
  
  return formatDate(dateString)
}

/**
 * Check if a deadline is urgent (within 7 days)
 */
export function isDeadlineUrgent(deadline: string): boolean {
  const deadlineDate = new Date(deadline)
  const now = new Date()
  const diffInDays = Math.floor((deadlineDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
  
  return diffInDays <= 7 && diffInDays >= 0
}

/**
 * Get days until deadline
 */
export function getDaysUntilDeadline(deadline: string): number {
  const deadlineDate = new Date(deadline)
  const now = new Date()
  return Math.floor((deadlineDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
}

/**
 * Truncate text to a specified length
 */
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text
  return text.slice(0, maxLength) + '...'
}

// Made with Bob
