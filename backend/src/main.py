from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from redis import Redis

from .core.config import get_settings
from .core.logger import setup_logging
from .core.database import create_tables
from .core.websocket import ConnectionManager
from .api.game import router as game_router
from .api.group import router as group_router

# Initialize settings and services
settings = get_settings()
# redis_client = Redis(host="0.0.0.0", port=6379, decode_responses=True)
# connection_manager = ConnectionManager(redis_client)

# Setup logging
setup_logging()
logger = logging.getLogger("globetrotter")

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(game_router, prefix="/api/v1")
app.include_router(group_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    try:
        # Initialize database
        await create_tables()
        logger.info("Database tables created successfully")

        # Test Redis connection
        # redis_ping = redis_client.ping()
        # logger.info(f"Redis connection test: {'Success' if redis_ping else 'Failed'}")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise


# @app.on_event("shutdown")
# async def shutdown_event():
#     logger.info(f"Shutting down {settings.PROJECT_NAME}")
#     redis_client.close()


@app.get("/")
async def root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
    }
