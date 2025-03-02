#!/usr/bin/env python
import os
import sys
import asyncio
import logging

# Add the parent directory to the path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sqlalchemy.ext.asyncio import create_async_engine
from src.models.base import Base
from src.core.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("recreate_db")

settings = get_settings()


async def recreate_database():
    """Recreate the database with a new name."""
    # Create a new database file name
    new_db_file = "globetrotter_new.db"
    new_db_url = f"sqlite+aiosqlite:///{new_db_file}"

    logger.info(f"Creating new database: {new_db_file}")

    # Create a new engine with the new database
    engine = create_async_engine(new_db_url, echo=False, future=True)

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info(f"Database tables created successfully in {new_db_file}")
    logger.info(f"To use this database, update your .env file with:")
    logger.info(f"DATABASE_URL=sqlite+aiosqlite:///{new_db_file}")


if __name__ == "__main__":
    # Run the async function
    asyncio.run(recreate_database())
