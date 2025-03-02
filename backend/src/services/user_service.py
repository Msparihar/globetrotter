from typing import Optional


class UserService:
    def __init__(self):
        # For demo purposes, using in-memory storage
        self.users = {}
        self.next_id = 1

    def create_user(self, username: str) -> dict:
        # Check if username already exists
        existing_user = self._find_by_username(username)
        if existing_user:
            return existing_user

        user = {"id": self.next_id, "username": username, "correct_answers": 0, "total_attempts": 0, "score": 0.0}
        self.users[self.next_id] = user
        self.next_id += 1
        return user

    def get_user_stats(self, username: str) -> Optional[dict]:
        user = self._find_by_username(username)
        if not user:
            return None
        return {"username": user["username"], "score": user["score"], "total_attempts": user["total_attempts"]}

    def update_user_stats(self, user_id: int, is_correct: bool) -> Optional[dict]:
        user = self.users.get(user_id)
        if not user:
            return None

        user["total_attempts"] += 1
        if is_correct:
            user["correct_answers"] += 1
        user["score"] = (user["correct_answers"] / user["total_attempts"]) * 100

        return user

    def _find_by_username(self, username: str) -> Optional[dict]:
        return next((user for user in self.users.values() if user["username"] == username), None)
