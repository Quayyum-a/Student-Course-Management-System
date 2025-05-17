from src.domain.user import User


class Facilitator(User):
    def __init__(self, full_name, email, password):
        super().__init__(full_name, email, password, role='facilitator')
        self.created_courses = []
