from src.domain.course import Course
from src.exceptions import (
    InvalidFormatError, 
    EmptyFieldError, 
    FileOperationError
)

class CourseService:
    def __init__(self, course_repository):
        self.course_repository = course_repository

    def create_course(self, course_id, name, facilitator_email):
        """Create a new course with the given ID, name, and facilitator."""
        if not course_id or not course_id.isalnum():
            raise InvalidFormatError("Course ID must be non-empty and alphanumeric")
        if not name.strip():
            raise EmptyFieldError("Course name cannot be empty")
        course = Course(course_id, name, facilitator_email)
        self.course_repository.save_course(course)
        return True

    def get_all_courses(self):
        """Retrieve all courses from the repository."""
        try:
            with open(self.course_repository.filename, 'r') as file:
                courses = []
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        courses.append(Course(parts[0], parts[1], parts[2]))
                return courses
        except FileNotFoundError:
            # Gracefully handle missing file by returning empty list
            # We could raise FileOperationError here, but returning empty list is more user-friendly
            return []
