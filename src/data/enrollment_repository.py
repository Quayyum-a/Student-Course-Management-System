class EnrollmentRepository:
    def __init__(self, filename):
        self.filename = filename

    def save_enrollment(self, course_id, student_email, grade=None):
        with open(self.filename, 'a') as file:
            file.write(f"{course_id},{student_email},{grade or ''}\n")

    def find_enrollments_by_student(self, student_email):
        enrollments = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) >= 2 and parts[1] == student_email:
                        enrollments.append({
                            'course_id': parts[0],
                            'student_email': parts[1],
                            'grade': parts[2] if len(parts) > 2 and parts[2] else None
                        })
            return enrollments
        except FileNotFoundError:
            return []