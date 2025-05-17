import os
import unittest

from src.data.course_repository import CourseRepository
from src.service.course_service import CourseService


class TestCourseService(unittest.TestCase):
    def setUp(self):
        self.filename = "test_courses.txt"
        self.repo = CourseRepository(self.filename)
        self.service = CourseService(self.repo)
        open(self.filename, 'w').close()

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_create_course(self):
        result = self.service.create_course("Python", "Array", "sikiru@gmail.com")
        self.assertTrue(result)
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            self.assertEqual(len(lines), 1)
            self.assertEqual(lines[0].strip(), "Python,Array,sikiru@gmail.com")

    def test_get_all_courses(self):
        self.service.create_course("Python", "Array", "sikiru@gmail.com")
        courses = self.service.get_all_courses()
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].course_id, "Python")
        self.assertEqual(courses[0].name, "Array")
        self.assertEqual(courses[0].facilitator_email, "sikiru@gmail.com")

    def test_get_all_courses_empty(self):
        courses = self.service.get_all_courses()
        self.assertEqual(courses, [])

if __name__ == '__main__':
    unittest.main()
