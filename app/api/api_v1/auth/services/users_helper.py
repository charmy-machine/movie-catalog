from abc import ABC, abstractmethod


class AbstractUsersHelper(ABC):
    @abstractmethod
    def get_username_password(self, username: str) -> str | None:
        """
        Get password by username.

        :param username:
        :return: user password if username exists or None.
        """

    @classmethod
    def check_passwords_match(
        cls,
        password1: str,
        password2: str,
    ) -> bool:
        """
        Check if passwords match.

        :param password1:
        :param password2:
        :return: True if passwords match, False otherwise.
        """
        return password1 == password2

    def validate_user_password(
        self,
        username: str,
        password: str,
    ) -> bool:
        """
        Check if password is valid.

        :param username: - the user whose password needs to be verified.
        :param password: - password to validate.
        :return: True if password is correct, False otherwise.
        """
        db_password = self.get_username_password(username)

        if db_password is None:
            return False
        return self.check_passwords_match(
            password1=db_password,
            password2=password,
        )
