import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI Analyst MVP - Startup Analysis Platform',
  description: 'AI-powered startup analysis and investor memo generation',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="font-sans">
        <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
          {children}
        </main>
      </body>
    </html>
  )
}