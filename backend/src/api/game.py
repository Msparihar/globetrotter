from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.database import get_db
from ..services.game_service import GameService
from ..schemas.destination import GameQuestion, GameAnswer, GameResult
from ..schemas.user import UserCreate, UserResponse, UserStats
from ..models.user import User

router = APIRouter()


async def get_game_service(db: AsyncSession = Depends(get_db)) -> GameService:
    return GameService(db)


@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if username exists
    existing_user = await db.scalar(select(User).where(User.username == user.username))
    if existing_user:
        return existing_user

    # Create new user
    new_user = User(username=user.username)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get("/game/question", response_model=GameQuestion)
async def get_question(game_service: GameService = Depends(get_game_service)):
    return await game_service.create_game_question()


@router.post("/game/answer", response_model=GameResult)
async def check_answer(answer: GameAnswer, user_id: int, game_service: GameService = Depends(get_game_service)):
    return await game_service.check_answer(user_id, answer.alias, answer.answer)


@router.get("/users/{username}/stats", response_model=UserStats)
async def get_user_stats(username: str, game_service: GameService = Depends(get_game_service)):
    user = await game_service.get_user_stats(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserStats(username=user.username, score=user.score, total_attempts=user.total_attempts)
