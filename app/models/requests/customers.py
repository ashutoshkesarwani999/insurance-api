import re
from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, field_validator, StringConstraints


class RegisterUserRequest(BaseModel):
    """
    Pydantic model for Customer registration request.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password, must be 8-64 characters long.
        username (str): The user's chosen username, must be 3-64 characters long.
    """

    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8, max_length=64)]
    username: Annotated[str, StringConstraints(min_length=3, max_length=64)]

    @field_validator("password")
    def password_must_contain_special_characters(cls, v):
        """
        Validate that the password contains at least one special character.

        Args:
            v (str): The password to validate.

        Returns:
            str: The validated password.

        Raises:
            ValueError: If the password doesn't contain a special character.
        """
        if not re.search(r"[^a-zA-Z0-9]", v):
            raise ValueError("Password must contain special characters")
        return v

    @field_validator("password")
    def password_must_contain_numbers(cls, v):
        """
        Validate that the password contains at least one number.

        Args:
            v (str): The password to validate.

        Returns:
            str: The validated password.

        Raises:
            ValueError: If the password doesn't contain a number.
        """
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain numbers")
        return v

    @field_validator("password")
    def password_must_contain_uppercase(cls, v):
        """
        Validate that the password contains at least one uppercase character.

        Args:
            v (str): The password to validate.

        Returns:
            str: The validated password.

        Raises:
            ValueError: If the password doesn't contain an uppercase character.
        """
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain uppercase characters")
        return v

    @field_validator("password")
    def password_must_contain_lowercase(cls, v):
        """
        Validate that the password contains at least one lowercase character.

        Args:
            v (str): The password to validate.

        Returns:
            str: The validated password.

        Raises:
            ValueError: If the password doesn't contain a lowercase character.
        """
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain lowercase characters")
        return v

    @field_validator("username")
    def username_must_not_contain_special_characters(cls, v):
        """
        Validate that the username does not contain any special characters.

        Args:
            v (str): The username to validate.

        Returns:
            str: The validated username.

        Raises:
            ValueError: If the username contains any special characters.
        """
        if re.search(r"[^a-zA-Z0-9]", v):
            raise ValueError("Username must not contain special characters")
        return v


class LoginCustomerRequest(BaseModel):
    """
    Pydantic model for customer login request.

    Attributes:
        email (EmailStr): The customer's email address.
        password (str): The customer's password.
    """

    email: EmailStr
    password: str
