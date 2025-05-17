import unittest
import os
from src.data.user_repository import UserRepository
from src.domain.user import User
from src.service.auth_service import AuthService

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
        user = User("Quayyum Ariyo", "quayyum@gmail.com", "password123")
        result = self.service.register_user(user)
        self.assertTrue(result)
        saved_user = self.repo.find_user_by_email("quayyum@gmail.com")
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.full_name, "Quayyum Ariyo")
        self.assertEqual(saved_user.email, "quayyum@gmail.com")
        self.assertEqual(saved_user.password, "password123")

    def test_register_user_duplicate_email(self):
        user1 = User("User One", "dup@example.com", "pass123")
        user2 = User("User Two", "dup@example.com", "pass456")
        result1 = self.service.register_user(user1)
        self.assertTrue(result1)
        with self.assertRaises(ValueError):
            self.service.register_user(user2)

if __name__ == '__main__':
    unittest.main()