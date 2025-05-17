from src.domain.facilitator import Facilitator
from src.domain.student import Student


class UserRepository:
    def __init__(self, filename):
        self.filename = filename

    def save_user(self, user):
        with open(self.filename, 'a') as file:
            file.write(f"{user.full_name},{user.email},{user.password},{user.role}\n")

    def find_user_by_email(self, email):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 4 and parts[1] == email:
                        role = parts[3]
                        if role == "student":
                            return Student(parts[0], parts[1], parts[2])
                        elif role == "facilitator":
                            return Facilitator(parts[0], parts[1], parts[2])
                return None
        except FileNotFoundError:
            return None