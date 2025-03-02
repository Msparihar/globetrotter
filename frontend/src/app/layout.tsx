'use client';

import { useEffect, useState } from "react";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from './providers';

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // Suppress hydration warnings
  const [mounted, setMounted] = useState(false);
  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen bg-gradient-to-b from-blue-900 to-blue-950 text-white relative overflow-x-hidden`} suppressHydrationWarning>
        <div
          className="absolute inset-0 bg-repeat opacity-10 pointer-events-none z-0"
          style={{ backgroundImage: 'url(/pattern.svg)' }}
        />
        <div className="relative z-10">
          <Providers>{children}</Providers>
        </div>

        {/* Decorative floating globes */}
        <div className="fixed -bottom-20 -left-20 w-40 h-40 rounded-full bg-blue-500/10 animate-float pointer-events-none" />
        <div className="fixed top-20 -right-10 w-32 h-32 rounded-full bg-blue-400/10 animate-float [animation-delay:2s] pointer-events-none" />
        <div className="fixed top-1/2 -left-16 w-32 h-32 rounded-full bg-blue-300/10 animate-float [animation-delay:4s] pointer-events-none" />
        <div className="fixed -bottom-10 right-20 w-24 h-24 rounded-full bg-blue-600/10 animate-float [animation-delay:1s] pointer-events-none" />
        <div className="fixed top-10 left-1/4 w-16 h-16 rounded-full bg-blue-200/10 animate-float [animation-delay:3s] pointer-events-none" />
      </body>
    </html>
  );
}
