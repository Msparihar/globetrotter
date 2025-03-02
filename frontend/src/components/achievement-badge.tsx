'use client';

import { motion } from 'framer-motion';
import { getRank } from '@/lib/constants';

interface AchievementBadgeProps {
  score: number;
}

export function AchievementBadge({ score }: AchievementBadgeProps) {
  const currentRank = getRank(score);
  const progressToNextRank = score;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      className="flex flex-col items-center p-4 rounded-lg bg-accent/10 backdrop-blur-sm border border-accent/20"
    >
      <span className="text-4xl mb-2">{currentRank.icon}</span>
      <h3 className="text-lg font-semibold text-center text-gray-900 dark:text-white">{currentRank.title}</h3>
      <div className="mt-2 w-full bg-background/50 rounded-full h-2 overflow-hidden">
        <motion.div
          className="h-full bg-primary"
          initial={{ width: 0 }}
          animate={{ width: `${progressToNextRank}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        />
      </div>
      <p className="text-sm text-gray-600 dark:text-gray-300 mt-2">
        {score < 100
          ? `${score}% progress`
          : "Maximum rank achieved!"}
      </p>
    </motion.div>
  );
}
