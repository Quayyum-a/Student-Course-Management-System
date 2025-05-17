from src.domain.course import Course

class CourseService:
    def __init__(self, course_repository):
        self.course_repository = course_repository

    def create_course(self, course_id, name, facilitator_email):
        course = Course(course_id, name, facilitator_email)
        self.course_repository.save_course(course)
        return True