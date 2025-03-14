'use client';

import { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AchievementBadge } from './achievement-badge';
import confetti from 'canvas-confetti';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { User } from '@/lib/types';
import { ShareDialog } from './share-dialog';
import { useQuestion, useSubmitAnswer, useUserStats, queryKeys } from '@/hooks/use-game-queries';
import { useQueryClient } from '@tanstack/react-query';
import { getUserStats } from '@/lib/api';
import Image from 'next/image';

interface GameProps {
  user: User;
}

export function Game({ user: initialUser }: GameProps) {
  const queryClient = useQueryClient();
  const [isShareOpen, setIsShareOpen] = useState(false);

  // Keep user stats in sync
  const { data: updatedStats, isLoading: isLoadingStats } = useUserStats(initialUser.username);
  console.log("updatedStats", updatedStats);
  console.log("isLoadingStats", isLoadingStats);

  // Merge initial user data with updated stats, preferring updated stats when available
  const user = useMemo(() => ({
    ...initialUser,
    ...(updatedStats && {
      score: updatedStats.score,
      total_attempts: updatedStats.total_attempts,
      correct_answers: updatedStats.score > 0
        ? Math.round((updatedStats.score * updatedStats.total_attempts) / 100)
        : 0
    })
  }), [initialUser, updatedStats]);

  const {
    data: question,
    isLoading: isLoadingQuestion,
    error: questionError,
    refetch: refetchQuestion
  } = useQuestion();

  const {
    mutate: submitAnswer,
    data: result,
    isPending: isSubmitting,
    reset: resetResult
  } = useSubmitAnswer();

  const handleAnswer = (answer: string) => {
    if (!question || isSubmitting) return;

    submitAnswer(
      { userId: user.id, answer: { alias: question.alias, answer } },
      {
        onSuccess: (result) => {
          if (result.is_correct) {
            // First burst from bottom
            confetti({
              particleCount: 100,
              spread: 70,
              origin: { y: 0.6 },
              colors: ['#4299E1', '#3182CE', '#2B6CB0', '#FBD38D', '#F6AD55']
            });

            // Delayed second burst from both sides
            setTimeout(() => {
              // Left side burst
              confetti({
                particleCount: 50,
                angle: 60,
                spread: 55,
                origin: { x: 0, y: 0.65 },
                colors: ['#4299E1', '#3182CE', '#2B6CB0', '#FBD38D', '#F6AD55']
              });
              // Right side burst
              confetti({
                particleCount: 50,
                angle: 120,
                spread: 55,
                origin: { x: 1, y: 0.65 },
                colors: ['#4299E1', '#3182CE', '#2B6CB0', '#FBD38D', '#F6AD55']
              });
            }, 300);
          }
        },
      }
    );
  };

  const handleNextQuestion = () => {
    resetResult();
    refetchQuestion();
  };

  if (questionError) {
    return (
      <Card className="w-full max-w-2xl bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-white/20 dark:border-gray-700/20 shadow-xl">
        <CardContent className="p-8 text-center">
          <div className="text-5xl mb-4">😢</div>
          <p className="text-red-500 text-lg mb-4">Failed to load question. Please try again.</p>
          <Button onClick={() => refetchQuestion()} className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white">
            Try Again
          </Button>
        </CardContent>
      </Card>
    );
  }

  // Create default messages for correct and incorrect answers
  const getResultMessage = (result: any) => {
    if (!result) return '';

    if (result.is_correct) {
      return result.message || `You correctly identified ${result.correct_answer}!`;
    } else {
      return result.message || `The correct answer was ${result.correct_answer}.`;
    }
  };

  return (
    <div className="w-full max-w-2xl space-y-6 p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Card className="backdrop-blur-md bg-white/80 dark:bg-gray-900/80 border-white/20 dark:border-gray-700/20 shadow-xl overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600"></div>
          <CardHeader className="pb-2">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div className="space-y-2">
                <CardTitle className="text-2xl sm:text-3xl font-bold flex items-center gap-2 text-gray-900 dark:text-white">
                  <span className="relative w-8 h-8">
                    <Image
                      src="/globe.svg"
                      alt="Globe"
                      width={32}
                      height={32}
                      className="animate-spin-slow"
                    />
                  </span>
                  Welcome, {user.username}!
                </CardTitle>
                <CardDescription className="text-base text-gray-600 dark:text-gray-300">
                  Your Journey: {user.correct_answers}/{user.total_attempts} destinations discovered
                </CardDescription>
                <AchievementBadge score={user.score || 0} />
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-8 p-6">
            {question && !result && (
              <AnimatePresence mode="wait">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="space-y-8"
                >
                  <div className="space-y-5 relative">
                    <motion.div
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      className="px-5 py-3 bg-indigo-100 dark:bg-indigo-900/30 rounded-lg inline-flex items-center"
                    >
                      <span className="text-xl mr-2">🧭</span>
                      <span className="font-medium text-gray-900 dark:text-white">
                        Where in the world is this place?
                      </span>
                    </motion.div>

                    {question.clues.map((clue, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.2 }}
                        className="clue-card bg-gradient-to-r from-white/90 to-white/70 dark:from-gray-800/90 dark:to-gray-800/70"
                      >
                        <p className="text-lg flex items-center gap-3 text-gray-900 dark:text-white">
                          <span className="text-2xl">{index === 0 ? '🗺️' : '🔍'}</span>
                          {clue}
                        </p>
                      </motion.div>
                    ))}
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {question.options.map((option) => (
                      <motion.div
                        key={option}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        <Button
                          onClick={() => handleAnswer(option)}
                          disabled={isSubmitting}
                          variant="outline"
                          className="option-button w-full h-auto py-5 text-lg bg-white/50 dark:bg-gray-800/50 hover:bg-blue-100 hover:text-blue-700 dark:hover:bg-blue-900/30 dark:hover:text-blue-300 border-white/20 dark:border-gray-700/20 text-gray-900 dark:text-white"
                        >
                          <span className="relative z-10">{option}</span>
                        </Button>
                      </motion.div>
                    ))}
                  </div>
                </motion.div>
              </AnimatePresence>
            )}

            {result && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="space-y-8"
              >
                <motion.div
                  className={`p-6 rounded-xl ${
                    result.is_correct
                      ? 'bg-gradient-to-br from-green-100/90 to-emerald-100/80 dark:from-green-900/30 dark:to-emerald-900/20'
                      : 'bg-gradient-to-br from-red-100/90 to-orange-100/80 dark:from-red-900/30 dark:to-orange-900/20'
                  } backdrop-blur-sm border border-white/20 dark:border-gray-700/20 shadow-lg`}
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ type: "spring", stiffness: 300, damping: 20 }}
                >
                  <div className="flex items-center gap-4 mb-4">
                    <div className={`text-5xl ${result.is_correct ? 'animate-bounce' : ''}`}>
                      {result.is_correct ? '🎉' : '✈️'}
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
                        {result.is_correct ? 'Great job, explorer!' : 'Not quite there yet...'}
                      </h3>
                      <p className="text-gray-700 dark:text-gray-300 mt-1">
                        {getResultMessage(result)}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 mt-4 bg-white/50 dark:bg-gray-800/50 p-3 rounded-lg">
                    <span className="text-lg">🌍</span>
                    <p className="font-medium text-lg text-gray-900 dark:text-white">
                      Destination: <span className="font-bold">{result.correct_answer}</span>
                    </p>
                  </div>

                  {result.fun_fact && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.3 }}
                      className="mt-6 p-4 bg-white/60 dark:bg-gray-800/40 rounded-lg border border-white/30 dark:border-gray-700/30"
                    >
                      <p className="flex items-start gap-3 text-gray-800 dark:text-gray-200">
                        <span className="text-xl mt-1">📝</span>
                        <span className="font-medium">{result.fun_fact}</span>
                      </p>
                    </motion.div>
                  )}
                </motion.div>

                <div className="flex gap-4 mt-6">
                  <Button
                    onClick={handleNextQuestion}
                    className="flex-1 card-hover bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white"
                  >
                    <span className="mr-2">🗺️</span>
                    Next Destination
                  </Button>
                  <Button
                    onClick={() => setIsShareOpen(true)}
                    variant="outline"
                    className="flex-1 card-hover bg-white/60 dark:bg-gray-800/60 hover:bg-blue-50 dark:hover:bg-blue-900/30 border-white/20 dark:border-gray-700/20 text-gray-900 dark:text-white"
                  >
                    <span className="mr-2">🌟</span>
                    Challenge Friends
                  </Button>
                </div>
              </motion.div>
            )}

            {isLoadingQuestion && (
              <div className="flex flex-col items-center justify-center py-12 space-y-6">
                <div className="relative">
                  <Image
                    src="/globe.svg"
                    alt="Globe"
                    width={60}
                    height={60}
                    className="animate-spin"
                  />
                </div>
                <p className="text-gray-700 dark:text-gray-300 animate-pulse text-lg">
                  Exploring the world map...
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </motion.div>

      <ShareDialog
        open={isShareOpen}
        onOpenChange={setIsShareOpen}
        username={user.username}
        score={user.score}
      />
    </div>
  );
}
