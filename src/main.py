from src.data.user_repository import UserRepository
from src.data.course_repository import CourseRepository
from src.data.enrollment_repository import EnrollmentRepository
from src.service.auth_service import AuthService
from src.service.course_service import CourseService
from src.service.enrollment_service import EnrollmentService
from src.presentation.console_app import ConsoleApp

def main():
    user_repo = UserRepository("data/users.txt")
    course_repo = CourseRepository("data/courses.txt")
    enrollment_repo = EnrollmentRepository("data/enrollments.txt")

    auth_service = AuthService(user_repo)
    course_service = CourseService(course_repo)
    enrollment_service = EnrollmentService(enrollment_repo, course_repo)

    app = ConsoleApp(auth_service, course_service, enrollment_service)
    app.start()

if __name__ == "__main__":
    main()