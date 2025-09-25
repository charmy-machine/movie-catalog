from abc import ABC, abstractmethod
import secrets

from redis import Redis

from core import config


class AbstractTokensHelper(ABC):
    @abstractmethod
    def token_exists(self, token: str) -> bool:
        """
        Check if token exists.
        :param token:
        :return:
        """

    @abstractmethod
    def save_token(self, token: str) -> None:
        """
        Save token in storage.
        :param token:
        :return:
        """

    @classmethod
    def generate_token(cls) -> str:
        """
        Generate token.
        :return:
        """
        return secrets.token_urlsafe(16)

    def generate_token_and_save(self, token: str) -> str:
        """
        Generate token and save it in storage.
        :return:
        """
        token = self.generate_token()
        self.save_token(token)
        return token


class RedisTokensHelper(AbstractTokensHelper):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        tokens_set_name: str,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )

        self.tokens_set_name = tokens_set_name

    def token_exists(self, token: str) -> bool:
        return bool(self.redis.sismember(self.tokens_set_name, token))

    def save_token(self, token: str) -> None:
        self.redis.sadd(self.tokens_set_name, token)


redis_tokens = RedisTokensHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    tokens_set_name=config.REDIS_TOKENS_SET_NAME,
)
