from src.domain.user import User


class Student(User):
    def __init__(self, email, password, name):
        super().__init__(email, password, name)
        self.enrolled_courses = []