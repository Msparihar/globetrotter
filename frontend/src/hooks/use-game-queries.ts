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
    mutationFn: async ({
      userId,
      answer,
    }: {
      userId: number;
      answer: GameAnswer;
    }) => {
      // First submit the answer
      const result = await submitAnswer(userId, answer);

      // Get the current user data from cache
      const user = queryClient.getQueryData<User>(["user", userId]);
      if (user) {
        // Then fetch updated stats
        const updatedStats = await getUserStats(user.username);
        // Update stats in cache
        queryClient.setQueryData(
          queryKeys.userStats(user.username),
          updatedStats
        );
      }

      return result;
    },
  });
}

// Get user stats
export function useUserStats(username: string) {
  return useQuery({
    queryKey: queryKeys.userStats(username),
    queryFn: () => getUserStats(username),
    enabled: !!username,
  });
}
