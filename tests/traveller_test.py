import unittest
from models.traveller import Traveller

class TestUserClass(unittest.TestCase):
    def setUp(self):
        self.new_user = Traveller("Xavier", "Brown")

    def test_user_has_first_name(self):
        self.assertEqual("Xavier", self.new_user.first_name)

    def test_user_has_last_name(self):
        self.assertEqual("Brown", self.new_user.last_name)