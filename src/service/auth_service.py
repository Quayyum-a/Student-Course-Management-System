import re


class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register_user(self, user):
        """Register a new user if the email is unique and valid."""
        if not self._is_valid_email(user.email):
            raise ValueError("Invalid email format")
        if not user.full_name.strip():
            raise ValueError("Full name cannot be empty")
        if not user.password.strip():
            raise ValueError("Password cannot be empty")
        existing_user = self.user_repository.find_user_by_email(user.email)
        if existing_user:
            raise ValueError("Email already registered")
        self.user_repository.save_user(user)
        return True

    def login_user(self, email, password):
        """Authenticate a user with email and password."""
        if not email or not password:
            raise ValueError("Email and password cannot be empty")
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        user = self.user_repository.find_user_by_email(email)
        if user and user.password == password:
            return user
        return None

    def _is_valid_email(self, email):
        """Validate email format using regex."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))