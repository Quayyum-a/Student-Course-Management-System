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
            print("\n1. Login\n2. Register\n3. Exit")
            choice = input("Enter choice: ")
            if choice == "1":
                self.login()
            elif choice == "2":
                self.register()
            elif choice == "3":
                break

    def register(self):
        full_name = input("Full Name: ")
        email = input("Email: ")
        password = input("Password: ")
        role = input("Role (student/Facilitator): ").lower()
        try:
            if role == "student":
                user = Student(full_name, email, password)
            elif role == "facilitator":
                user = Facilitator(full_name, email, password)
            else:
                print("Invalid role")
                return
            if self.auth_service.register_user(user):
                print("Registration successful!")
        except ValueError as e:
            print(f"Error: {e}")

    def login(self):
        email = input("Email: ")
        password = input("Password: ")
        user = self.auth_service.login_user(email, password)
        if user:
            self.current_user = user
            print(f"Welcome, {user.full_name}!")
            self.show_menu()
        else:
            print("Invalid credentials")

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
                print(f"Course ID: {course.course_id}, Name: {course.name}, Facilitator: {course.Facilitator_email}")
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
        course_id = input("Enter Course ID: ")
        try:
            if self.enrollment_service.enroll_student(course_id, self.current_user.email):
                print("Enrollment successful!")
        except ValueError as e:
            print(f"Error: {e}")

    def create_course(self):
        course_id = input("Enter Course ID: ")
        name = input("Enter Course Name: ")
        try:
            if self.course_service.create_course(course_id, name, self.current_user.email):
                print("Course created successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    def assign_grade(self):
        course_id = input("Enter Course ID: ")
        student_email = input("Enter Student Email: ")
        grade = input("Enter Grade: ")
        try:
            if self.enrollment_service.assign_grade(course_id, student_email, grade):
                print("Grade assigned successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    def view_enrolled_students(self):
        course_id = input("Enter Course ID: ")
        students = self.enrollment_service.get_course_students(course_id)
        if students:
            for student in students:
                print(f"Student Email: {student['student_email']}, Grade: {student['grade'] or 'Not graded'}")
        else:
            print("No students enrolled")