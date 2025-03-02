import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createUser, getQuestion, submitAnswer, getUserStats } from "@/lib/api";
import { GameAnswer, GameResult, User } from "@/lib/types";

// Query keys
export const queryKeys = {
  question: ["question"],
  userStats: (username: string) => ["userStats", username],
} as const;

// Get current question
export function useQuestion() {
  return useQuery({
    queryKey: queryKeys.question,
    queryFn: getQuestion,
    staleTime: 1000 * 60 * 5, // Consider the question stale after 5 minutes
  });
}

// Create user mutation
export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (username: string) => createUser(username),
    onSuccess: (data: User) => {
      // Optionally invalidate relevant queries or update cache
      queryClient.invalidateQueries({
        queryKey: queryKeys.userStats(data.username),
      });
    },
  });
}

// Submit answer mutation
export function useSubmitAnswer() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ userId, answer }: { userId: number; answer: GameAnswer }) =>
      submitAnswer(userId, answer),
    onSuccess: (gameResult: GameResult, variables) => {
      // Get the current user data from the cache
      const user = queryClient.getQueryData<User>(["user", variables.userId]);

      if (user) {
        // Invalidate both question and user stats
        queryClient.invalidateQueries({ queryKey: queryKeys.question });
        queryClient.invalidateQueries({
          queryKey: queryKeys.userStats(user.username),
        });
      }
    },
  });
}

// Get user stats
export function useUserStats(username: string) {
  return useQuery({
    queryKey: queryKeys.userStats(username),
    queryFn: () => getUserStats(username),
    enabled: !!username, // Only run the query if we have a username
  });
}
