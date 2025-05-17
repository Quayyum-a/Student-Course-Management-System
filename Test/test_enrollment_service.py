import os
import unittest

from src.data.course_repository import CourseRepository
from src.data.enrollment_repository import EnrollmentRepository
from src.service.course_service import CourseService
from src.service.enrollment_service import EnrollmentService


class TestEnrollmentService(unittest.TestCase):
    def setUp(self):
        self.course_filename = "test_courses.txt"
        self.enrollment_filename = "test_enrollments.txt"
        self.course_repo = CourseRepository(self.course_filename)
        self.enrollment_repo = EnrollmentRepository(self.enrollment_filename)
        self.course_service = CourseService(self.course_repo)
        self.service = EnrollmentService(self.enrollment_repo, self.course_repo)
        open(self.course_filename, 'w').close()
        open(self.enrollment_filename, 'w').close()

    def tearDown(self):
        for filename in [self.course_filename, self.enrollment_filename]:
            if os.path.exists(filename):
                os.remove(filename)

    def test_enroll_student(self):
        self.course_service.create_course("Python", "Array", "sikiru@gmail.com")
        result = self.service.enroll_student("Python", "quayyum@gmail.com")
        self.assertTrue(result)
        with open(self.enrollment_filename, 'r') as file:
            lines = file.readlines()
            self.assertEqual(len(lines), 1)
            self.assertEqual(lines[0].strip(), "Python,quayyum@gmail.com,")

    def test_enroll_student_course_not_found(self):
        with self.assertRaises(ValueError):
            self.service.enroll_student("CS999", "quayyum@gmail.com")

    def test_assign_grade(self):
        self.course_service.create_course("Python", "Array", "sikiru@gmail.com")
        self.service.enroll_student("Python", "quayyum@gmail.com")
        result = self.service.assign_grade("Python", "quayyum@gmail.com", "A")
        self.assertTrue(result)
        enrollments = self.service.get_student_grades("quayyum@gmail.com")
        self.assertEqual(enrollments[0]['grade'], "A")

    def test_get_student_courses(self):
        self.course_service.create_course("Python", "Array", "sikiru@gmail.com")
        self.service.enroll_student("Python", "quayyum@gmail.com")
        courses = self.service.get_student_courses("quayyum@gmail.com")
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].course_id, "Python")

    def test_get_course_students(self):
        self.course_service.create_course("Python", "Array", "sikiru@gmail.com")
        self.service.enroll_student("Python", "student1@example.com")
        self.service.enroll_student("Python", "student2@example.com")
        students = self.service.get_course_students("Python")
        self.assertEqual(len(students), 2)
        self.assertEqual(students[0]['student_email'], "student1@example.com")
        self.assertEqual(students[1]['student_email'], "student2@example.com")

if __name__ == '__main__':
    unittest.main()
