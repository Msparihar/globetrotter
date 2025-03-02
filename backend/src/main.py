from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .core.config import get_settings
from .core.logger import setup_logging
from .core.database import create_tables
from .api.game import router as game_router

# Initialize settings
settings = get_settings()

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
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(game_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    try:
        await create_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


@app.get("/")
async def root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
    }
