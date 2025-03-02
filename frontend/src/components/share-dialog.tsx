'use client';

import { useState, useMemo } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { generateShareImage } from '@/lib/api';
import Image from 'next/image';
import { motion } from 'framer-motion';
import { getRank } from '@/lib/constants';

interface ShareDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  username: string;
  score: number;
}

export function ShareDialog({
  open,
  onOpenChange,
  username,
  score,
}: ShareDialogProps) {
  const [isCopied, setIsCopied] = useState(false);
  const currentRank = useMemo(() => getRank(score), [score]);

  const shareUrl = `${window.location.origin}?invite=${encodeURIComponent(
    username
  )}`;
  const shareImage = generateShareImage(username, score);

  const shareText = `I'm a ${currentRank.title} ${currentRank.icon} with ${score}% on Globetrotter! Can you beat my score?`;

  const handleShare = async () => {
    const shareData = {
      title: '🌍 Globetrotter Challenge',
      text: shareText,
      url: shareUrl,
    };

    try {
      if (navigator.share) {
        await navigator.share(shareData);
      } else if (navigator.clipboard) {
        await navigator.clipboard.writeText(shareUrl);
        setIsCopied(true);
        setTimeout(() => setIsCopied(false), 2000);
      }
    } catch (err) {
      console.error('Error sharing:', err);
    }
  };

  const handleWhatsAppShare = () => {
    const text = encodeURIComponent(`${shareText} ${shareUrl}`);
    window.open(`https://wa.me/?text=${text}`, '_blank');
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Share Your Achievement!</DialogTitle>
        </DialogHeader>
        <div className="space-y-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-accent/10 p-4 rounded-lg backdrop-blur-sm border border-accent/20 text-center"
          >
            <span className="text-4xl block mb-2">{currentRank.icon}</span>
            <h3 className="text-lg font-semibold">{currentRank.title}</h3>
            <p className="text-sm text-muted-foreground mt-1">
              with a score of {score}%
            </p>
          </motion.div>
          <div className="aspect-video relative rounded-lg overflow-hidden bg-muted">
            <Image
              src={shareImage}
              alt="Share preview"
              fill
              className="object-cover"
              priority
            />
          </div>
          <div className="flex flex-col gap-4">
            <Button onClick={handleWhatsAppShare} className="w-full">
              <span className="mr-2">📱</span> Share on WhatsApp
            </Button>
            <Button
              onClick={handleShare}
              variant="outline"
              className="w-full"
            >
              {isCopied ? '✅ Copied!' : '🔗 Copy Invite Link'}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
