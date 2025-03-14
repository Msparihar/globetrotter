from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str
    max_players: int = 10


class GroupCreate(GroupBase):
    pass


class GroupMemberBase(BaseModel):
    score: int = 0


class GroupMemberCreate(GroupMemberBase):
    pass


class GroupMember(GroupMemberBase):
    group_id: str
    user_id: int
    joined_at: datetime

    class Config:
        from_attributes = True


class Group(GroupBase):
    id: str
    creator_id: int
    created_at: datetime
    active: bool

    class Config:
        from_attributes = True


class GroupWithMembers(Group):
    members: List[GroupMember] = []

    class Config:
        from_attributes = True


class GameRoundBase(BaseModel):
    group_id: str
    destination_id: int


class GameRoundCreate(GameRoundBase):
    pass


class PlayerAnswerBase(BaseModel):
    answer: str


class PlayerAnswerCreate(PlayerAnswerBase):
    pass


class PlayerAnswer(PlayerAnswerBase):
    round_id: int
    user_id: int
    is_correct: bool
    answered_at: datetime

    class Config:
        from_attributes = True


class GameRound(GameRoundBase):
    id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    player_answers: List[PlayerAnswer] = []

    class Config:
        from_attributes = True


# WebSocket message schemas
class WebSocketMessage(BaseModel):
    type: str
    data: dict


class JoinGroupMessage(BaseModel):
    group_id: str
    user_id: int


class StartRoundMessage(BaseModel):
    group_id: str


class SubmitAnswerMessage(BaseModel):
    group_id: str
    user_id: int
    round_id: int
    answer: str


class GroupStats(BaseModel):
    total_players: int
    active_players: int
    rounds_played: int
    current_round: Optional[int] = None
