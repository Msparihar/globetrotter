import random
from typing import List, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.destination import Destination
from ..models.user import User
from ..schemas.destination import GameQuestion, GameResult


class GameService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_random_destination(self) -> Tuple[Destination, List[str]]:
        # Get total count of destinations
        count = await self.db.scalar(select(func.count()).select_from(Destination))

        # Get random offset
        offset = random.randint(0, count - 1)

        # Get random destination
        destination = await self.db.scalar(select(Destination).offset(offset).limit(1))

        # Get 3 random wrong options
        wrong_options = await self.db.scalars(
            select(Destination.name).where(Destination.name != destination.name).order_by(func.random()).limit(3)
        )

        # Combine correct and wrong options and shuffle
        options = list(wrong_options.all()) + [destination.name]
        random.shuffle(options)

        return destination, options

    async def create_game_question(self) -> GameQuestion:
        destination, options = await self.get_random_destination()

        # Select 1-2 random clues
        num_clues = random.randint(1, 2)
        selected_clues = random.sample(destination.clues, num_clues)

        return GameQuestion(alias=destination.alias, clues=selected_clues, options=options)

    async def check_answer(self, user_id: int, alias: str, answer: str) -> GameResult:
        # Get destination
        destination = await self.db.scalar(select(Destination).where(Destination.alias == alias))

        if not destination:
            return GameResult(
                is_correct=False,
                correct_answer="Unknown",
                fun_fact="",
                user_score=0,
                message="Error: Destination not found.",
            )

        is_correct = destination.name.lower() == answer.lower()

        # Update user stats
        user = await self.db.scalar(select(User).where(User.id == user_id))
        if not user:
            return GameResult(
                is_correct=False,
                correct_answer=destination.name,
                fun_fact="",
                user_score=0,
                message="Error: User not found.",
            )

        user.total_attempts += 1

        # Create appropriate message based on answer correctness
        message = ""

        if is_correct:
            user.correct_answers += 1
            message = f"Correct! {destination.name} is the right answer. Well done!"
        else:
            message = f"Incorrect. The correct answer is {destination.name}. Try again!"

        await self.db.commit()

        # Get random fun fact
        fun_fact = random.choice(destination.fun_facts) if is_correct else ""

        return GameResult(
            is_correct=is_correct,
            correct_answer=destination.name,
            fun_fact=fun_fact,
            user_score=user.score,
            message=message,
        )

    async def get_user_stats(self, username: str) -> User:
        return await self.db.scalar(select(User).where(User.username == username))
