export interface GameQuestion {
  alias: string;
  clues: string[];
  options: string[];
}

export interface GameAnswer {
  alias: string;
  answer: string;
}

export interface GameResult {
  is_correct: boolean;
  correct_answer: string;
  fun_fact: string;
  user_score: number | null;
}

export interface UserStats {
  username: string;
  score: number;
  total_attempts: number;
}

export interface User {
  id: number;
  username: string;
  correct_answers: number;
  total_attempts: number;
  score: number;
}
