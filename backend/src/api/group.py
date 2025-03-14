from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis

from ..core.database import get_db
from ..core.websocket import ConnectionManager
from ..services.group_service import GroupService
from ..schemas.group import (
    Group,
    GroupWithMembers,
    GroupCreate,
    GroupMember,
    GameRound,
    PlayerAnswer,
    PlayerAnswerCreate,
    GroupStats,
    WebSocketMessage,
)
from ..core.logger import logger

router = APIRouter()

# Initialize Redis and ConnectionManager
redis_client = Redis(host="localhost", port=6379, decode_responses=True)
logger.info(f"Redis client initialized: {redis_client}")
connection_manager = ConnectionManager(redis_client)


async def get_group_service(db: AsyncSession = Depends(get_db)) -> GroupService:
    return GroupService(db, connection_manager)


@router.post("/groups", response_model=GroupWithMembers)
async def create_group(
    group_data: GroupCreate,
    user_id: int,
    group_service: GroupService = Depends(get_group_service),
):
    """Create a new group."""
    return await group_service.create_group(group_data, user_id)


@router.get("/groups/{group_id}", response_model=GroupWithMembers)
async def get_group(
    group_id: str,
    group_service: GroupService = Depends(get_group_service),
):
    """Get group details."""
    group = await group_service.get_group(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.post("/groups/{group_id}/join")
async def join_group(
    group_id: str,
    user_id: int,
    group_service: GroupService = Depends(get_group_service),
):
    """Join an existing group."""
    success, message = await group_service.join_group(group_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}


@router.post("/groups/{group_id}/start", response_model=GameRound)
async def start_round(
    group_id: str,
    creator_id: int,
    group_service: GroupService = Depends(get_group_service),
):
    """Start a new game round."""
    success, message, game_round = await group_service.start_round(group_id, creator_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return game_round


@router.post("/rounds/{round_id}/answer", response_model=PlayerAnswer)
async def submit_answer(
    round_id: int,
    user_id: int,
    answer_data: PlayerAnswerCreate,
    group_service: GroupService = Depends(get_group_service),
):
    """Submit an answer for the current round."""
    success, message, player_answer = await group_service.submit_answer(round_id, user_id, answer_data.answer)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return player_answer


@router.get("/groups/{group_id}/leaderboard")
async def get_leaderboard(
    group_id: str,
    group_service: GroupService = Depends(get_group_service),
):
    """Get the group's leaderboard."""
    return await group_service.get_leaderboard(group_id)


@router.websocket("/ws/{group_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    group_id: str,
    user_id: str,
):
    """WebSocket endpoint for real-time game updates."""
    try:
        await connection_manager.connect(websocket, group_id, user_id)
        while True:
            try:
                # Wait for messages from the client
                data = await websocket.receive_json()
                message = WebSocketMessage(**data)

                # Broadcast the message to all connected clients in the group
                await connection_manager.broadcast_to_group(group_id, message.dict())
            except WebSocketDisconnect:
                await connection_manager.disconnect(group_id, user_id)
                break
    except Exception as e:
        await connection_manager.disconnect(group_id, user_id)
        raise HTTPException(status_code=500, detail=str(e))
