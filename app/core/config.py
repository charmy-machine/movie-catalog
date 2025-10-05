import logging


LOGGER_LEVEL = logging.INFO
LOGGER_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

REDIS_HOST: str = "localhost"
REDIS_PORT: int = 6379
REDIS_DB: int = 0
REDIS_DB_TOKENS: int = 2
REDIS_DB_USERS: int = 4
REDIS_DB_MOVIES: int = 6

REDIS_TOKENS_SET_NAME = "tokens"
REDIS_MOVIES_HASH_NAME = "movies"
