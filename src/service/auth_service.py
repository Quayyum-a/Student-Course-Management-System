import re
from src.exceptions import (
    InvalidEmailError, 
    EmptyFieldError, 
    ResourceAlreadyExistsError
)


class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register_user(self, user):
        if not self._is_valid_email(user.email):
            raise InvalidEmailError("Invalid email format")
        if not user.full_name.strip():
            raise EmptyFieldError("Full name cannot be empty")
        if not user.password.strip():
            raise EmptyFieldError("Password cannot be empty")
        existing_user = self.user_repository.find_user_by_email(user.email)
        if existing_user:
            raise ResourceAlreadyExistsError("Email already registered")
        self.user_repository.save_user(user)
        return True

    def login_user(self, email, password):
        if not email or not password:
            raise EmptyFieldError("Email and password cannot be empty")
        if not self._is_valid_email(email):
            raise InvalidEmailError("Invalid email format")
        user = self.user_repository.find_user_by_email(email)
        if user and user.password == password:
            return user
        return None

    def _is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
