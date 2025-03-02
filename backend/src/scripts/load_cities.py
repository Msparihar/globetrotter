#!/usr/bin/env python
import json
import os
import sys
import asyncio
import logging
import random
import string

# Add the parent directory to the path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sqlalchemy import select, func, delete
from src.models.destination import Destination
from src.core.config import get_settings
from src.core.database import AsyncSessionLocal, create_tables

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("load_cities")

settings = get_settings()


def generate_alias(city_name: str) -> str:
    """Generate a unique alias for a city (up to 10 chars)."""
    # Use the first 3 letters of the city name as a base
    base = city_name[:3].lower()

    # Add random characters to make it unique and match the required length
    random_chars = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))

    return f"{base}{random_chars}"


async def load_cities():
    """Load city data from JSON file into the database."""
    # Create tables if they don't exist
    await create_tables()

    # Read data from JSON file
    try:
        data_path = settings.DATA_FILE_PATH
        logger.info(f"Reading data from {data_path}")

        with open(data_path, "r", encoding="utf-8") as f:
            cities_data = json.load(f)

        logger.info(f"Found {len(cities_data)} cities in data file")

        # Create a session
        async with AsyncSessionLocal() as session:
            # Check for existing data
            existing_count = await session.scalar(select(func.count()).select_from(Destination))
            logger.info(f"Found {existing_count} existing cities in database")

            # Delete existing data if requested
            if len(sys.argv) > 1 and sys.argv[1] == "--reset":
                logger.warning("Resetting existing city data...")
                await session.execute(delete(Destination))
                await session.commit()
                logger.info("Existing city data deleted")

            # Insert data
            inserted = 0
            for city_data in cities_data:
                # Generate a unique alias for each city
                alias = generate_alias(city_data["city"])

                # Check if we already have this city in the database
                existing = await session.scalar(select(Destination).where(Destination.name == city_data["city"]))

                if existing:
                    logger.info(f"City {city_data['city']} already exists, skipping")
                    continue

                # Create new destination object
                destination = Destination(
                    alias=alias,
                    name=city_data["city"],
                    country=city_data["country"],
                    clues=city_data["clues"],
                    fun_facts=city_data["fun_fact"],  # Note: JSON key is "fun_fact" but model is "fun_facts"
                )

                # Add to session
                session.add(destination)
                inserted += 1

            # Commit all changes
            await session.commit()
            logger.info(f"Successfully inserted {inserted} cities into database")
    except FileNotFoundError:
        logger.error(f"Data file not found at {settings.DATA_FILE_PATH}")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in {settings.DATA_FILE_PATH}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading city data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Run the async function
    asyncio.run(load_cities())
