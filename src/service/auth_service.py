class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register_user(self, user):
        existing_user = self.user_repository.find_user_by_email(user.email)
        if existing_user:
            raise ValueError("Email already registered")
        self.user_repository.save_user(user)
        return True

    def login_user(self, email, password):
        user = self.user_repository.find_user_by_email(email)
        if user and user.password == password:
            return user
        return None