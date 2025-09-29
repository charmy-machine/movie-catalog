from pathlib import Path
import logging

BASE_DIR = Path(__file__).resolve().parent.parent
MOVIES_STORAGE_FILEPATH = BASE_DIR / "movies.json"

LOGGER_LEVEL = logging.INFO
LOGGER_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

REDIS_HOST: str = "localhost"
REDIS_PORT: int = 6379
REDIS_DB: int = 0
REDIS_DB_TOKENS: int = 2
REDIS_DB_USERS: int = 4

REDIS_TOKENS_SET_NAME = "tokens"
