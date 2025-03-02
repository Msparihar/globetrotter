# Globetrotter Backend

A scalable FastAPI backend for the Globetrotter geography quiz game.

## Features

- Random geography quiz questions from a curated list of cities
- Multiple choice answers with fun facts for correct answers
- City lookup by country
- Comprehensive logging system with rotating file handler
- Easy to extend with new cities and questions

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs with Python
- **Pydantic**: Data validation using Python type annotations
- **Python Logging**: Built-in logging with rotating file handler
- **PostgreSQL**: Primary database (planned for user stats)
- **Docker**: Containerization for easy deployment

## Project Structure

```
backend/
├── src/
│   ├── api/              # API routes and endpoints
│   │   └── v1/
│   │       └── quiz.py   # Quiz-related endpoints
│   ├── core/             # Core application code
│   │   ├── config.py     # Configuration management
│   │   └── logger.py     # Logging configuration
│   ├── services/         # Business logic
│   │   └── quiz.py       # Quiz service
│   └── main.py          # Application entry point
├── data/
│   └── data.json        # Quiz data
├── tests/               # Test suite
├── logs/               # Application logs
├── pyproject.toml      # Project dependencies
└── README.md          # This file
```

## Setup and Installation

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -e ".[dev]"
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Start the development server:

```bash
uvicorn src.main:app --reload
```

## API Endpoints

### Quiz Endpoints

#### Get Random Question

```http
GET /api/v1/quiz/question
```

Response:

```json
{
    "city": "Paris",
    "country": "France",
    "clues": [
        "This city is home to a famous tower that sparkles every night.",
        "Known as the 'City of Love' and a hub for fashion and art."
    ],
    "options": ["London", "Paris", "Berlin", "Rome"]
}
```

#### Submit Answer

```http
POST /api/v1/quiz/answer
Content-Type: application/json

{
    "city": "Paris",
    "answer": "Paris"
}
```

Response:

```json
{
    "correct": true,
    "correct_answer": "Paris",
    "fun_fact": "The Eiffel Tower was supposed to be dismantled after 20 years but was saved because it was useful for radio transmissions!"
}
```

#### Get Cities by Country

```http
GET /api/v1/quiz/cities/{country}
```

Response:

```json
[
    {
        "city": "Paris",
        "country": "France",
        "clues": [...],
        "fun_fact": [...]
    }
]
```

## Development

### Adding New Cities

Add new cities to `data/data.json` following this format:

```json
{
    "city": "City Name",
    "country": "Country Name",
    "clues": [
        "First clue about the city",
        "Second clue about the city"
    ],
    "fun_fact": [
        "Interesting fact about the city",
        "Another interesting fact"
    ],
    "trivia": [
        "Additional trivia about the city",
        "More trivia"
    ]
}
```

### Logging

Logs are stored in the `logs` directory with the following features:

- Rotation: Every 500MB
- Maximum backups: 10 files
- Log format: Timestamp, logger name, level, and message
- Console output: Standard output stream
- File output: Rotating log files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a pull request

## License

MIT License
