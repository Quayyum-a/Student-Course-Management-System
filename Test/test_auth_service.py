import os
import unittest

from src.data.user_repository import UserRepository
from src.domain.facilitator import Facilitator
from src.domain.student import Student
from src.service.auth_service import AuthService
from src.exceptions import InvalidEmailError, EmptyFieldError, ResourceAlreadyExistsError


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.filename = "test_users.txt"
        self.repo = UserRepository(self.filename)
        self.service = AuthService(self.repo)
        # Ensure the test file exists and is empty
        open(self.filename, 'w').close()

    def tearDown(self):
        # Clean up the test file after each test
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_register_user_unique_email(self):
        user = Student("Quayyum Ariyo", "quayyum@gmail.com", "password123")
        result = self.service.register_user(user)
        self.assertTrue(result)
        saved_user = self.repo.find_user_by_email("quayyum@gmail.com")
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.full_name, "Quayyum Ariyo")
        self.assertEqual(saved_user.email, "quayyum@gmail.com")
        self.assertEqual(saved_user.password, "password123")
        self.assertEqual(saved_user.role, "student")

    def test_register_user_duplicate_email(self):
        user1 = Student("User One", "dup@example.com", "pass123")
        user2 = Facilitator("User Two", "dup@example.com", "pass456")
        result1 = self.service.register_user(user1)
        self.assertTrue(result1)
        with self.assertRaises(ResourceAlreadyExistsError):
            self.service.register_user(user2)

    def test_register_user_invalid_email(self):
        user = Student("Test User", "invalid_email", "pass123")
        with self.assertRaises(InvalidEmailError):
            self.service.register_user(user)

    def test_register_user_empty_fields(self):
        user = Student("", "test@example.com", "pass123")
        with self.assertRaises(EmptyFieldError):
            self.service.register_user(user)
        user = Student("Test User", "test@example.com", "")
        with self.assertRaises(EmptyFieldError):
            self.service.register_user(user)

    def test_login_user_success(self):
        user = Student("Test User", "test@example.com", "pass123")
        self.service.register_user(user)
        logged_in_user = self.service.login_user("test@example.com", "pass123")
        self.assertIsNotNone(logged_in_user)
        self.assertEqual(logged_in_user.email, "test@example.com")
        self.assertEqual(logged_in_user.role, "student")

    def test_login_user_invalid_password(self):
        user = Student("Test User", "test@example.com", "pass123")
        self.service.register_user(user)
        logged_in_user = self.service.login_user("test@example.com", "wrongpass")
        self.assertIsNone(logged_in_user)

    def test_login_user_nonexistent_email(self):
        logged_in_user = self.service.login_user("nonexistent@example.com", "pass123")
        self.assertIsNone(logged_in_user)

    def test_login_user_invalid_email(self):
        with self.assertRaises(InvalidEmailError):
            self.service.login_user("invalid_email", "pass123")

    def test_login_user_empty_input(self):
        with self.assertRaises(EmptyFieldError):
            self.service.login_user("", "pass123")
        with self.assertRaises(EmptyFieldError):
            self.service.login_user("test@example.com", "")

if __name__ == '__main__':
    unittest.main()
