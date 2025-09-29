import secrets
from abc import ABC, abstractmethod


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
