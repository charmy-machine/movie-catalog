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

    @classmethod
    def generate_token(cls) -> str:
        """
        Generate token.
        :return:
        """
        return secrets.token_urlsafe(16)

    def generate_token_and_save(self) -> str:
        """
        Generate token and save it in storage.
        :return:
        """
        token = self.generate_token()
        self.save_token(token)
        return token

    @abstractmethod
    def save_token(self, token: str) -> None:
        """
        Save token in storage.
        :param token:
        :return:
        """

    @abstractmethod
    def get_tokens(self) -> list[str]:
        """
        Get all tokens.
        :return:
        """

    @abstractmethod
    def delete_token(self, token: str) -> None:
        """
        Delete passed token from storage.
        :param token:
        :return:
        """
