import re

from src.domain.facilitator import Facilitator
from src.domain.student import Student


class ConsoleApp:
    def __init__(self, auth_service, course_service, enrollment_service):
        self.auth_service = auth_service
        self.course_service = course_service
        self.enrollment_service = enrollment_service
        self.current_user = None

    def start(self):
        while True:
            print("\nChoose Role:")
            print("1. Student")
            print("2. Facilitator")
            print("3. Exit")
            role_choice = input("Enter choice (1-3): ")
            if role_choice == "3":
                break
            if role_choice not in ["1", "2"]:
                print("Invalid role choice")
                continue
            role = "student" if role_choice == "1" else "facilitator"
            print(f"\n{role.capitalize()} Menu:")
            print("1. Login")
            print("2. Register")
            print("3. Back")
            action_choice = input("Enter choice (1-3): ")
            if action_choice == "1":
                self.login(role)
            elif action_choice == "2":
                self.register(role)
            elif action_choice == "3":
                continue

    def register(self, role):
        full_name = input("Full Name: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        try:
            if not full_name:
                raise ValueError("Full name cannot be empty")
            if not self._is_valid_email(email):
                raise ValueError("Invalid email format")
            if not password:
                raise ValueError("Password cannot be empty")
            user = Student(full_name, email, password) if role == "student" else Facilitator(full_name, email, password)
            if self.auth_service.register_user(user):
                print("Registration successful!")
        except ValueError as e:
            print(f"Error: {e}")

    def login(self, role):
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        try:
            user = self.auth_service.login_user(email, password)
            if user and user.role == role:
                self.current_user = user
                print(f"Welcome, {user.full_name}!")
                self.show_menu()
            else:
                print("Invalid credentials or role mismatch")
        except ValueError as e:
            print(f"Error: {e}")

    def show_menu(self):
        while True:
            if isinstance(self.current_user, Student):
                print("\nStudent Menu:")
                print("1. View Enrolled Courses")
                print("2. View Grades")
                print("3. Enroll in Course")
                print("4. Logout")
                choice = input("Enter choice: ")
                if choice == "1":
                    self.view_enrolled_courses()
                elif choice == "2":
                    self.view_grades()
                elif choice == "3":
                    self.enroll_in_course()
                elif choice == "4":
                    self.current_user = None
                    break
            elif isinstance(self.current_user, Facilitator):
                print("\nFacilitator Menu:")
                print("1. Create Course")
                print("2. Assign Grade")
                print("3. View Enrolled Students")
                print("4. Logout")
                choice = input("Enter choice: ")
                if choice == "1":
                    self.create_course()
                elif choice == "2":
                    self.assign_grade()
                elif choice == "3":
                    self.view_enrolled_students()
                elif choice == "4":
                    self.current_user = None
                    break

    def view_enrolled_courses(self):
        courses = self.enrollment_service.get_student_courses(self.current_user.email)
        if courses:
            for course in courses:
                print(f"Course ID: {course.course_id}, Name: {course.name}, Facilitator: {course.instructor_email}")
        else:
            print("No enrolled courses")

    def view_grades(self):
        enrollments = self.enrollment_service.get_student_grades(self.current_user.email)
        if enrollments:
            for enrollment in enrollments:
                grade = enrollment['grade'] if enrollment['grade'] else "Not graded"
                print(f"Course ID: {enrollment['course_id']}, Grade: {grade}")
        else:
            print("No grades available")

    def enroll_in_course(self):
        course_id = input("Enter Course ID: ").strip()
        try:
            if not course_id:
                raise ValueError("Course ID cannot be empty")
            if not course_id.isalnum():
                raise ValueError("Course ID must be alphanumeric")
            if self.enrollment_service.enroll_student(course_id, self.current_user.email):
                print("Enrollment successful!")
        except ValueError as e:
            print(f"Error: {e}")

    def create_course(self):
        course_id = input("Enter Course ID: ").strip()
        name = input("Enter Course Name: ").strip()
        try:
            if not course_id:
                raise ValueError("Course ID cannot be empty")
            if not course_id.isalnum():
                raise ValueError("Course ID must be alphanumeric")
            if not name:
                raise ValueError("Course name cannot be empty")
            if self.course_service.create_course(course_id, name, self.current_user.email):
                print("Course created successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    def assign_grade(self):
        course_id = input("Enter Course ID: ").strip()
        student_email = input("Enter Student Email: ").strip()
        grade = input("Enter Grade: ").strip()
        try:
            if not course_id:
                raise ValueError("Course ID cannot be empty")
            if not course_id.isalnum():
                raise ValueError("Course ID must be alphanumeric")
            if not self._is_valid_email(student_email):
                raise ValueError("Invalid student email format")
            if not grade:
                raise ValueError("Grade cannot be empty")
            if not self._is_valid_grade(grade):
                raise ValueError("Grade must be a valid letter grade (e.g., A, B, C)")
            if self.enrollment_service.assign_grade(course_id, student_email, grade):
                print("Grade assigned successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    def view_enrolled_students(self):
        course_id = input("Enter Course ID: ").strip()
        try:
            if not course_id:
                raise ValueError("Course ID cannot be empty")
            if not course_id.isalnum():
                raise ValueError("Course ID must be alphanumeric")
            students = self.enrollment_service.get_course_students(course_id)
            if students:
                for student in students:
                    print(f"Student Email: {student['student_email']}, Grade: {student['grade'] or 'Not graded'}")
            else:
                print("No students enrolled")
        except ValueError as e:
            print(f"Error: {e}")

    def _is_valid_email(self, email):
        """Validate email format using regex."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def _is_valid_grade(self, grade):
        """Validate grade format (e.g., A, B, C, etc.)."""
        valid_grades = ['A', 'B', 'C', 'D', 'F', 'A+', 'A-', 'B+', 'B-', 'C+', 'C-', 'D+', 'D-']
        return grade in valid_grades