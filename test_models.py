from unittest import TestCase
from models import User

class UserTestCase(TestCase):
    """Tests for User class"""
    def test_get_full_name(self):
        user1 = User(first_name="Bertrand", last_name="Russell")
        user2 = User(first_name="Plato")

        self.assertEqual(user1.get_full_name(), "Bertrand Russell")
        self.assertEqual(user2.get_full_name(), "Plato")
