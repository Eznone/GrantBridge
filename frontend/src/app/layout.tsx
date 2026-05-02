import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

import './globals.css'
import { cn } from '@/lib/utils/cn'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
})

export const metadata: Metadata = {
  title: 'GrantBridge - AI Grant Assistant for NGOs',
  description:
    'Discover grants, manage applications, and generate funding proposals with AI assistance',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={cn('font-sans', inter.variable)}
    >
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}

// Made with Bob
