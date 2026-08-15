```tsx
import { Analytics } from '@vercel/analytics/next'
import type { Metadata, Viewport } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: {
    default: 'AI EV Management System',
    template: '%s | AI EV Management System',
  },

  description:
    'AI-powered Electric Vehicle Management System for intelligent traffic monitoring, EV tracking, charging station management, route optimization, and smart mobility.',

  keywords: [
    'AI EV Management System',
    'Electric Vehicle Management',
    'EV Traffic Management',
    'EV Charging Stations',
    'Smart Traffic Management',
    'Route Optimization',
    'Artificial Intelligence',
    'Smart Mobility',
  ],

  authors: [
    {
      name: 'AI EV Management System Team',
    },
  ],

  applicationName: 'AI EV Management System',

  icons: {
    icon: '/icon.svg',
    apple: '/apple-icon.png',
  },
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  colorScheme: 'light dark',

  themeColor: [
    {
      media: '(prefers-color-scheme: light)',
      color: '#ffffff',
    },
    {
      media: '(prefers-color-scheme: dark)',
      color: '#171717',
    },
  ],
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="antialiased">
        {children}

        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
```
