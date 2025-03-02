from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str


class UserResponse(BaseModel):
    id: int
    username: str
    correct_answers: int = 0
    total_attempts: int = 0
    score: float = 0.0


class UserStats(BaseModel):
    username: str
    score: float
    total_attempts: int
