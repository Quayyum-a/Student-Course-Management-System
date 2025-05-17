from src.domain.user import User

class UserRepository:
    def __init__(self, filename):
        self.filename = filename

    def save_user(self, user):
        with open(self.filename, 'a') as file:
            file.write(f"{user.full_name},{user.email},{user.password}\n")

    def find_user_by_email(self, email):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 3 and parts[1] == email:
                        return User(parts[0], parts[1], parts[2])
                return None
        except FileNotFoundError:
            return None