from datetime import datetime
from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    max_players: Mapped[int] = mapped_column(Integer, default=10)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    members = relationship("GroupMember", back_populates="group")
    rounds = relationship("GameRound", back_populates="group")
    creator = relationship("User", back_populates="created_groups")


class GroupMember(Base):
    __tablename__ = "group_members"

    group_id: Mapped[str] = mapped_column(String(10), ForeignKey("groups.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    score: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    group = relationship("Group", back_populates="members")
    user = relationship("User", back_populates="group_memberships")


class GameRound(Base):
    __tablename__ = "game_rounds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[str] = mapped_column(String(10), ForeignKey("groups.id"))
    destination_id: Mapped[int] = mapped_column(Integer, ForeignKey("destinations.id"))
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relationships
    group = relationship("Group", back_populates="rounds")
    destination = relationship("Destination")
    player_answers = relationship("PlayerAnswer", back_populates="round")


class PlayerAnswer(Base):
    __tablename__ = "player_answers"

    round_id: Mapped[int] = mapped_column(Integer, ForeignKey("game_rounds.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    answer: Mapped[str] = mapped_column(String(100))
    is_correct: Mapped[bool] = mapped_column(Boolean)
    answered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    round = relationship("GameRound", back_populates="player_answers")
    user = relationship("User", back_populates="answers")
