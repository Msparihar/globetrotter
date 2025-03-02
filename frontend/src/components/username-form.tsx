'use client';

import { useState } from 'react';
import { generateUsername } from '@/lib/username-generator';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { User } from '@/lib/types';
import { useCreateUser } from '@/hooks/use-game-queries';
import { motion } from 'framer-motion';
import Image from 'next/image';

interface UsernameFormProps {
  onUserCreated: (user: User) => void;
}

export function UsernameForm({ onUserCreated }: UsernameFormProps) {
  const [username, setUsername] = useState('');

  const {
    mutate: createUser,
    isPending,
    error
  } = useCreateUser();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim()) return;

    createUser(username, {
      onSuccess: (user) => {
        onUserCreated(user);
      },
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="w-[350px] sm:w-[400px] backdrop-blur-md bg-white/80 dark:bg-gray-900/80 border-white/20 dark:border-gray-700/20 shadow-xl">
        <CardHeader className="space-y-4 text-center">
          <div className="mx-auto relative w-20 h-20">
            <Image
              src="/globe.svg"
              alt="Globetrotter Logo"
              width={80}
              height={80}
              className="animate-float"
            />
          </div>
          <CardTitle className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400">
            Globetrotter
          </CardTitle>
          <CardDescription className="text-lg text-gray-600 dark:text-gray-300">
            Your world geography adventure awaits!
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
          <div className="flex gap-2">
            <Input
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={isPending}
              className="w-full h-12 text-lg bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border-white/20 dark:border-gray-700/20 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
              minLength={3}
              maxLength={50}
              required
            />
            <Button
              type="button"
              variant="outline"
              onClick={() => setUsername(generateUsername())}
              disabled={isPending}
              className="h-12 whitespace-nowrap bg-white/50 dark:bg-gray-800/50 text-black hover:bg-blue-100 hover:text-blue-700 dark:hover:bg-blue-900/30 dark:hover:text-blue-300"
            >
              <span className="mr-2">🎲</span>
              Generate
            </Button>
          </div>
              {error && (
                <motion.p
                  className="text-sm text-red-500"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                >
                  Failed to create user. Please try again.
                </motion.p>
              )}
            </div>
            <Button
              type="submit"
              className="w-full h-12 text-lg bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-lg"
              disabled={isPending || !username.trim()}
            >
              {isPending ? (
                <div className="flex items-center justify-center">
                  <div className="mr-2 h-4 w-4 rounded-full border-2 border-white border-t-transparent animate-spin"></div>
                  Creating...
                </div>
              ) : (
                <div className="flex items-center justify-center">
                  <span className="mr-2">🚀</span> Start Your Journey
                </div>
              )}
            </Button>
          </form>
        </CardContent>
        <CardFooter className="text-center text-sm text-gray-600 dark:text-gray-300">
          Explore cities around the world and test your geography knowledge!
        </CardFooter>
      </Card>
    </motion.div>
  );
}
