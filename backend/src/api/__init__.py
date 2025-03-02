from fastapi import APIRouter
from .game import router as game_router

api_router = APIRouter(prefix="/api/v1")

# Include all route modules here
api_router.include_router(game_router)
