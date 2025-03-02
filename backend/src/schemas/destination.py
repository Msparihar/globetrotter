from typing import List
from pydantic import BaseModel, Field


class DestinationBase(BaseModel):
    alias: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=100)
    clues: List[str] = Field(..., min_items=1)
    fun_facts: List[str] = Field(..., min_items=1)


class DestinationCreate(DestinationBase):
    pass


class DestinationResponse(DestinationBase):
    id: int

    class Config:
        from_attributes = True


class GameQuestion(BaseModel):
    alias: str
    clues: List[str]
    options: List[str]  # List of possible destination names to choose from


class GameAnswer(BaseModel):
    alias: str
    answer: str


class GameResult(BaseModel):
    is_correct: bool
    correct_answer: str
    fun_fact: str
    user_score: float | None = None
    message: str
