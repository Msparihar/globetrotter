#!/usr/bin/env python
import os
import sys
import asyncio
import logging

# Add the parent directory to the path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sqlalchemy import select
from src.models.destination import Destination
from src.core.database import AsyncSessionLocal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("list_cities")


async def list_cities():
    """List all cities in the database."""
    try:
        # Create a session
        async with AsyncSessionLocal() as session:
            # Query all cities ordered by name
            query = select(Destination).order_by(Destination.name)
            result = await session.execute(query)
            destinations = result.scalars().all()

            # Print the results
            print(f"\nFound {len(destinations)} cities in the database:\n")
            print("ID  | ALIAS    | CITY                | COUNTRY")
            print("-" * 60)
            for dest in destinations:
                print(f"{dest.id:<4}| {dest.alias:<9}| {dest.name:<20}| {getattr(dest, 'country', 'N/A')}")

            print("\n")
    except Exception as e:
        logger.error(f"Error listing cities: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Run the async function
    asyncio.run(list_cities())
