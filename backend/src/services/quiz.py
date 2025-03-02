import json
import logging
import random
from typing import Any, Dict, List, Optional

from fastapi import HTTPException

from ..core.config import get_settings

settings = get_settings()
logger = logging.getLogger("globetrotter")


class QuizService:
    def __init__(self):
        self._data: Optional[List[Dict[str, Any]]] = None

    def _load_data(self) -> None:
        """Load quiz data from JSON file."""
        try:
            with open(settings.DATA_FILE_PATH, "r", encoding="utf-8") as f:
                self._data = json.load(f)
            logger.info(f"Successfully loaded {len(self._data)} cities from {settings.DATA_FILE_PATH}")
        except FileNotFoundError:
            logger.error(f"Quiz data file not found at {settings.DATA_FILE_PATH}")
            raise HTTPException(status_code=500, detail="Quiz data file not found")
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON format in {settings.DATA_FILE_PATH}")
            raise HTTPException(status_code=500, detail="Invalid quiz data format")

    @property
    def data(self) -> List[Dict[str, Any]]:
        """Get quiz data, loading it if not already loaded."""
        if self._data is None:
            self._load_data()
        return self._data

    def get_random_city(self) -> Dict[str, Any]:
        """Get a random city from the quiz data."""
        city_data = random.choice(self.data)
        logger.info(f"Selected city: {city_data['city']}")
        return city_data

    def get_city_by_name(self, city_name: str) -> Optional[Dict[str, Any]]:
        """Get city data by city name."""
        city = next((item for item in self.data if item["city"].lower() == city_name.lower()), None)
        if city:
            logger.info(f"Found city data for: {city_name}")
        else:
            logger.warning(f"City not found: {city_name}")
        return city

    def get_cities_by_country(self, country: str) -> List[Dict[str, Any]]:
        """Get all cities from a specific country."""
        cities = [item for item in self.data if item["country"].lower() == country.lower()]
        logger.info(f"Found {len(cities)} cities in {country}")
        return cities

    def get_random_question(self) -> Dict[str, Any]:
        """Generate a random question from the quiz data."""
        city_data = self.get_random_city()
        question = {
            "city": city_data["city"],
            "country": city_data["country"],
            "clues": city_data["clues"],
            "options": self._generate_options(city_data["city"]),
        }
        logger.info(f"Generated question for city: {city_data['city']}")
        return question

    def _generate_options(self, correct_city: str, num_options: int = 4) -> List[str]:
        """Generate multiple choice options including the correct city."""
        all_cities = [city["city"] for city in self.data if city["city"] != correct_city]
        options = random.sample(all_cities, k=min(num_options - 1, len(all_cities)))
        options.append(correct_city)
        random.shuffle(options)
        return options

    def verify_answer(self, city: str, answer: str) -> Dict[str, Any]:
        """Verify if the answer is correct for the given city."""
        city_data = self.get_city_by_name(city)
        if not city_data:
            logger.error(f"City not found for verification: {city}")
            raise HTTPException(status_code=404, detail="City not found")

        is_correct = city_data["city"].lower() == answer.lower()
        result = {
            "correct": is_correct,
            "correct_answer": city_data["city"],
            "fun_fact": random.choice(city_data["fun_fact"]) if is_correct else None,
        }
        logger.info(f"Answer verification for {city}: {'correct' if is_correct else 'incorrect'}")
        return result


# Create a singleton instance
quiz_service = QuizService()
