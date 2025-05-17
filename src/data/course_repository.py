from src.domain.course import Course

class CourseRepository:
    def __init__(self, filename):
        self.filename = filename

    def save_course(self, course):
        with open(self.filename, 'a') as file:
            file.write(f"{course.course_id},{course.name},{course.instructor_email}\n")

    def find_course_by_id(self, course_id):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 3 and parts[0] == course_id:
                        return Course(parts[0], parts[1], parts[2])
                return None
        except FileNotFoundError:
            return None