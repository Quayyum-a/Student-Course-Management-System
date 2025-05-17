class Course:
    def __init__(self, course_id, name, facilitator_email):
        self.course_id = course_id
        self.name = name
        self.facilitator_email = facilitator_email
        self.enrollments = {}  # Dictionary: student_email -> grade