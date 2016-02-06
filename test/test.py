from django.test import TestCase
from main.models import User

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(email="testcase@naver.com", username="mingkim")

    def test_animals_can_speak(self):
        user = User.objects.get(username="mingkim")
        self.assertEqual(user.get_full_name(), "testcase@naver.com")
