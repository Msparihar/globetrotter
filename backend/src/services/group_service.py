import random
import string
from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.group import Group, GroupMember, GameRound, PlayerAnswer
from ..models.user import User
from ..models.destination import Destination
from ..core.websocket import ConnectionManager
from ..schemas.group import GroupCreate, GroupMemberCreate, GameRoundCreate


class GroupService:
    def __init__(self, db: AsyncSession, connection_manager: ConnectionManager):
        self.db = db
        self.connection_manager = connection_manager

    async def generate_group_id(self, length: int = 6) -> str:
        """Generate a random group ID."""
        chars = string.ascii_uppercase + string.digits
        while True:
            group_id = "".join(random.choices(chars, k=length))
            # Check if ID already exists
            existing_group = await self.db.scalar(select(Group).where(Group.id == group_id))
            if not existing_group:
                return group_id

    async def create_group(self, group_data: GroupCreate, creator_id: int) -> Group:
        """Create a new group."""
        group_id = await self.generate_group_id()
        group = Group(id=group_id, name=group_data.name, creator_id=creator_id, max_players=group_data.max_players)
        self.db.add(group)

        # Add creator as first member
        member = GroupMember(group_id=group_id, user_id=creator_id)
        self.db.add(member)

        await self.db.commit()
        await self.db.refresh(group)
        return group

    async def get_group(self, group_id: str) -> Optional[Group]:
        """Get group by ID."""
        stmt = select(Group).where(Group.id == group_id).options(selectinload(Group.members))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def join_group(self, group_id: str, user_id: int) -> Tuple[bool, str]:
        """Join a group. Returns (success, message)."""
        group = await self.get_group(group_id)
        if not group:
            return False, "Group not found"

        if not group.active:
            return False, "Group is not active"

        # Check if user is already a member
        existing_member = await self.db.scalar(
            select(GroupMember).where(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
        )
        if existing_member:
            return True, "Already a member"

        # Check if group is full
        member_count = await self.db.scalar(
            select(func.count()).select_from(GroupMember).where(GroupMember.group_id == group_id)
        )
        if member_count >= group.max_players:
            return False, "Group is full"

        # Add new member
        member = GroupMember(group_id=group_id, user_id=user_id)
        self.db.add(member)
        await self.db.commit()

        return True, "Successfully joined group"

    async def start_round(self, group_id: str, creator_id: int) -> Tuple[bool, str, Optional[GameRound]]:
        """Start a new game round. Returns (success, message, round)."""
        group = await self.get_group(group_id)
        if not group:
            return False, "Group not found", None

        if group.creator_id != creator_id:
            return False, "Only the group creator can start rounds", None

        # Check if there's an active round
        active_round = await self.db.scalar(
            select(GameRound).where(GameRound.group_id == group_id, GameRound.ended_at.is_(None))
        )
        if active_round:
            return False, "A round is already in progress", None

        # Get random destination
        count = await self.db.scalar(select(func.count()).select_from(Destination))
        offset = random.randint(0, count - 1)
        destination = await self.db.scalar(select(Destination).offset(offset).limit(1))

        # Create new round
        game_round = GameRound(group_id=group_id, destination_id=destination.id)
        self.db.add(game_round)
        await self.db.commit()
        await self.db.refresh(game_round)

        # Prepare question data
        wrong_options = await self.db.scalars(
            select(Destination.name).where(Destination.name != destination.name).order_by(func.random()).limit(3)
        )

        options = list(wrong_options.all()) + [destination.name]
        random.shuffle(options)

        # Broadcast question to all players
        await self.connection_manager.broadcast_game_start(
            group_id,
            {
                "round_id": game_round.id,
                "alias": destination.alias,
                "clues": random.sample(destination.clues, min(len(destination.clues), 2)),
                "options": options,
            },
        )

        return True, "Round started successfully", game_round

    async def submit_answer(self, round_id: int, user_id: int, answer: str) -> Tuple[bool, str, Optional[PlayerAnswer]]:
        """Submit an answer for a round. Returns (success, message, answer)."""
        # Get the round
        game_round = await self.db.scalar(select(GameRound).where(GameRound.id == round_id))
        if not game_round:
            return False, "Round not found", None

        if game_round.ended_at:
            return False, "Round has ended", None

        # Check if user already answered
        existing_answer = await self.db.scalar(
            select(PlayerAnswer).where(PlayerAnswer.round_id == round_id, PlayerAnswer.user_id == user_id)
        )
        if existing_answer:
            return False, "Already submitted an answer", None

        # Get correct answer
        destination = await self.db.scalar(select(Destination).where(Destination.id == game_round.destination_id))
        is_correct = destination.name.lower() == answer.lower()

        # Record answer
        player_answer = PlayerAnswer(round_id=round_id, user_id=user_id, answer=answer, is_correct=is_correct)
        self.db.add(player_answer)

        # Update member score if correct
        if is_correct:
            await self.db.execute(
                update(GroupMember)
                .where(GroupMember.group_id == game_round.group_id, GroupMember.user_id == user_id)
                .values(score=GroupMember.score + 10)
            )

        await self.db.commit()
        await self.db.refresh(player_answer)

        # Check if all players have answered
        total_members = await self.db.scalar(
            select(func.count()).select_from(GroupMember).where(GroupMember.group_id == game_round.group_id)
        )
        total_answers = await self.db.scalar(
            select(func.count()).select_from(PlayerAnswer).where(PlayerAnswer.round_id == round_id)
        )

        # If all players have answered, end the round
        if total_answers >= total_members:
            game_round.ended_at = datetime.utcnow()
            await self.db.commit()

            # Get all answers and broadcast results
            answers = await self.db.scalars(select(PlayerAnswer).where(PlayerAnswer.round_id == round_id))

            results = {
                "round_id": round_id,
                "correct_answer": destination.name,
                "answers": [
                    {"user_id": answer.user_id, "is_correct": answer.is_correct, "answer": answer.answer}
                    for answer in answers
                ],
            }
            await self.connection_manager.broadcast_round_results(game_round.group_id, results)

        return True, "Answer submitted successfully", player_answer

    async def get_leaderboard(self, group_id: str) -> List[dict]:
        """Get group leaderboard."""
        members = await self.db.scalars(
            select(GroupMember).where(GroupMember.group_id == group_id).order_by(GroupMember.score.desc())
        )

        leaderboard = []
        for member in members:
            user = await self.db.scalar(select(User).where(User.id == member.user_id))
            leaderboard.append({"user_id": member.user_id, "username": user.username, "score": member.score})

        return leaderboard
