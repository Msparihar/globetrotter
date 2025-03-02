import { GameQuestion, GameAnswer, GameResult, User, UserStats } from "./types";
import { getRank } from "./constants";

const API_BASE = "http://localhost:8000/api/v1";

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  return response.json();
}

export async function createUser(username: string): Promise<User> {
  return fetchApi<User>("/users", {
    method: "POST",
    body: JSON.stringify({ username }),
  });
}

export async function getQuestion(): Promise<GameQuestion> {
  return fetchApi<GameQuestion>("/game/question");
}

export async function submitAnswer(
  userId: number,
  answer: GameAnswer
): Promise<GameResult> {
  return fetchApi<GameResult>(`/game/answer?user_id=${userId}`, {
    method: "POST",
    body: JSON.stringify(answer),
  });
}

export async function getUserStats(username: string): Promise<UserStats> {
  return fetchApi<UserStats>(`/users/${username}/stats`);
}

export function generateShareImage(username: string, score: number): string {
  const currentRank = getRank(score);
  // In a real app, you might want to generate this server-side
  // For now, we'll use a simple URL with query parameters
  const text = encodeURIComponent(
    `${currentRank.icon} ${currentRank.title}\n` +
      `Score: ${score}%\n` +
      `Can you beat @${username}'s score in Globetrotter?`
  );
  return `https://via.placeholder.com/600x400?text=${text}`;
}
