class EnrollmentService:
    def __init__(self, enrollment_repository, course_repository):
        self.enrollment_repository = enrollment_repository
        self.course_repository = course_repository

    def enroll_student(self, course_id, student_email):
        course = self.course_repository.find_course_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        self.enrollment_repository.save_enrollment(course_id, student_email)
        return True

    def assign_grade(self, course_id, student_email, grade):
        self.enrollment_repository.save_enrollment(course_id, student_email, grade)
        return True