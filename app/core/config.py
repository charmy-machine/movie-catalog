from pathlib import Path
import logging

BASE_DIR = Path(__file__).resolve().parent.parent
MOVIES_STORAGE_FILEPATH = BASE_DIR / "movies.json"

LOGGER_LEVEL = logging.INFO
LOGGER_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

# Never store real tokens here!
# Only fake values
API_TOKENS: frozenset[str] = frozenset(
    {
        "dhhI4evsuyyM75G8QaYXww",
        "ZjFMZQxI6BD4rKgiDd1Oiw",
    }
)
