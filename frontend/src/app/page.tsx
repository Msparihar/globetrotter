'use client';

import { useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { UsernameForm } from '@/components/username-form';
import { Game } from '@/components/game';
import type { User } from '@/lib/types';
import { Suspense } from 'react';
import { Header } from '@/components/ui/header';
import { Footer } from '@/components/ui/footer';
import { motion } from 'framer-motion';

export default function Home() {
  const [user, setUser] = useState<User | null>(null);

  return (
    <main className="min-h-screen flex flex-col items-center p-4 relative">
      <Header />

      <motion.div
        className="w-full max-w-4xl mx-auto flex-1 flex items-center justify-center z-10 my-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <Suspense fallback={
          <div className="flex items-center justify-center space-x-2">
            <div className="w-4 h-4 rounded-full bg-blue-500 animate-pulse"></div>
            <div className="w-4 h-4 rounded-full bg-blue-400 animate-pulse" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-4 h-4 rounded-full bg-blue-300 animate-pulse" style={{ animationDelay: '0.4s' }}></div>
          </div>
        }>
          <InviteSection user={user} setUser={setUser} />
        </Suspense>
      </motion.div>

      <Footer />
    </main>
  );
}

function InviteSection({ user, setUser }: { user: User | null; setUser: (user: User) => void }) {
  const searchParams = useSearchParams();
  const inviteUsername = searchParams.get('invite');

  return (
    <>
      {inviteUsername && !user && (
        <motion.div
          className="text-center mb-8 p-6 backdrop-blur-sm bg-white/10 rounded-xl border border-white/20 shadow-xl"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <div className="text-3xl mb-2">🎯</div>
          <h2 className="text-2xl font-bold mb-2">
            {inviteUsername} has challenged you!
          </h2>
          <p className="text-blue-200">
            Create a username to start playing and see if you can beat their score.
          </p>
        </motion.div>
      )}

      {!user ? (
        <div className="flex justify-center w-full">
          <UsernameForm onUserCreated={setUser} />
        </div>
      ) : (
        <Game user={user} />
      )}
    </>
  );
}
