from src.domain.user import User


class Student(User):
    def __init__(self, email, password, name):
        super().__init__(email, password, name, role = 'student')
        self.enrolled_courses = []