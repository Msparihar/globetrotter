#!/usr/bin/env python
import os
import sys
import asyncio
import logging
import json

# Add the parent directory to the path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.models.destination import Destination
from src.models.user import User
from src.models.group import Group, GroupMember, GameRound, PlayerAnswer
from src.core.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("recreate_db")

settings = get_settings()


def load_destination_data():
    """Load destination data from the JSON file."""
    data_file = os.path.join(os.path.dirname(__file__), "../../data/data.json")
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


def create_alias(city_name: str) -> str:
    """Create a unique alias from the city name."""
    # Remove spaces and special characters, take first 3 chars lowercase
    cleaned = "".join(c.lower() for c in city_name if c.isalnum())
    return cleaned[:3]


async def recreate_database():
    """Recreate the database with a new name and load initial data."""
    # Create a new database file name
    new_db_file = "globetrotter_new.db"
    new_db_url = f"sqlite+aiosqlite:///{new_db_file}"

    logger.info(f"Creating new database: {new_db_file}")

    # Create a new engine with the new database
    engine = create_async_engine(new_db_url, echo=False, future=True)

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Drop existing tables
        await conn.run_sync(Base.metadata.create_all)

    logger.info(f"Database tables created successfully in {new_db_file}")

    # Create an async session
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Load and insert destination data
    destinations_data = load_destination_data()
    async with async_session() as session:
        for city_data in destinations_data:
            destination = Destination(
                name=city_data["city"],
                alias=create_alias(city_data["city"]),
                country=city_data["country"],
                clues=city_data["clues"],
                fun_facts=city_data["fun_fact"],
            )
            session.add(destination)
        await session.commit()

    logger.info(f"Initial destination data loaded successfully")
    logger.info(f"To use this database, update your .env file with:")
    logger.info(f"DATABASE_URL=sqlite+aiosqlite:///{new_db_file}")


if __name__ == "__main__":
    # Run the async function
    asyncio.run(recreate_database())
