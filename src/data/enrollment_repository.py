class EnrollmentRepository:
    def __init__(self, filename):
        self.filename = filename

    def save_enrollment(self, course_id, student_email, grade=None):
        enrollments = self.find_all_enrollments()
        updated = False
        for enrollment in enrollments:
            if enrollment['course_id'] == course_id and enrollment['student_email'] == student_email:
                enrollment['grade'] = grade
                updated = True
                break
        if not updated:
            enrollments.append({
                'course_id': course_id,
                'student_email': student_email,
                'grade': grade
            })
        with open(self.filename, 'w') as file:
            for enrollment in enrollments:
                file.write(f"{enrollment['course_id']},{enrollment['student_email']},{enrollment['grade'] or ''}\n")

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

    def find_enrollments_by_course(self, course_id):
        enrollments = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) >= 2 and parts[0] == course_id:
                        enrollments.append({
                            'course_id': parts[0],
                            'student_email': parts[1],
                            'grade': parts[2] if len(parts) > 2 and parts[2] else None
                        })
            return enrollments
        except FileNotFoundError:
            return []

    def find_all_enrollments(self):
        enrollments = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        enrollments.append({
                            'course_id': parts[0],
                            'student_email': parts[1],
                            'grade': parts[2] if len(parts) > 2 and parts[2] else None
                        })
            return enrollments
        except FileNotFoundError:
            return []