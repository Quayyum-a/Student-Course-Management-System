import re
from src.exceptions import (
    InvalidEmailError, 
    InvalidFormatError, 
    ResourceNotFoundError, 
    EmptyFieldError,
    ResourceAlreadyExistsError
)


class EnrollmentService:
    def __init__(self, enrollment_repository, course_repository):
        self.enrollment_repository = enrollment_repository
        self.course_repository = course_repository

    def enroll_student(self, course_id, student_email):
        if not course_id or not course_id.isalnum():
            raise InvalidFormatError("Course ID must be non-empty and alphanumeric")
        if not self._is_valid_email(student_email):
            raise InvalidEmailError("Invalid student email format")
        course = self.course_repository.find_course_by_id(course_id)
        if not course:
            raise ResourceNotFoundError("Course not found")
        # Check if already enrolled
        enrollments = self.enrollment_repository.find_enrollments_by_student(student_email)
        if any(e['course_id'] == course_id for e in enrollments):
            return True  # Already enrolled, no action needed
        self.enrollment_repository.save_enrollment(course_id, student_email)
        return True

    def assign_grade(self, course_id, student_email, grade):
        if not course_id or not course_id.isalnum():
            raise InvalidFormatError("Course ID must be non-empty and alphanumeric")
        if not self._is_valid_email(student_email):
            raise InvalidEmailError("Invalid student email format")
        if not grade or not self._is_valid_grade(grade):
            raise InvalidFormatError("Grade must be a valid letter grade (e.g., A, B, C)")
        course = self.course_repository.find_course_by_id(course_id)
        if not course:
            raise ResourceNotFoundError("Course not found")
        # Check if student is enrolled
        enrollments = self.enrollment_repository.find_enrollments_by_student(student_email)
        if not any(e['course_id'] == course_id for e in enrollments):
            raise ResourceNotFoundError("Student not enrolled in this course")
        self.enrollment_repository.save_enrollment(course_id, student_email, grade)
        return True

    def get_student_courses(self, student_email):
        if not self._is_valid_email(student_email):
            raise InvalidEmailError("Invalid student email format")
        enrollments = self.enrollment_repository.find_enrollments_by_student(student_email)
        courses = []
        for enrollment in enrollments:
            course = self.course_repository.find_course_by_id(enrollment['course_id'])
            if course:
                courses.append(course)
        return courses

    def get_student_grades(self, student_email):
        if not self._is_valid_email(student_email):
            raise InvalidEmailError("Invalid student email format")
        return self.enrollment_repository.find_enrollments_by_student(student_email)

    def get_course_students(self, course_id):
        if not course_id or not course_id.isalnum():
            raise InvalidFormatError("Course ID must be non-empty and alphanumeric")
        course = self.course_repository.find_course_by_id(course_id)
        if not course:
            raise ResourceNotFoundError("Course not found")
        return self.enrollment_repository.find_enrollments_by_course(course_id)

    def _is_valid_email(self, email):
        """Validate email format using regex."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def _is_valid_grade(self, grade):
        """Validate grade format (e.g., A, B, C, etc.)."""
        valid_grades = ['A', 'B', 'C', 'D', 'F', 'A+', 'A-', 'B+', 'B-', 'C+', 'C-', 'D+', 'D-']
        return grade in valid_grades
