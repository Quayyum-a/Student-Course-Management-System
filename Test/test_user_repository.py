import os
import unittest

from src.data.user_repository import UserRepository
from src.domain.user import User


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.filename = "../test_users.txt"
        self.repo = UserRepository(self.filename)
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_save_user(self):
        user = User("Quayyum Ariyo", "quayyum@gmail.com", "password123")
        self.repo.save_user(user)
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            self.assertEqual(len(lines), 1)
            self.assertEqual(lines[0].strip(), "Quayyum Ariyo quayyum@gmail.com password123")

if __name__ == '__main__':
    unittest.main()
