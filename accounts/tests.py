from django.test import TestCase
from django.contrib.auth import get_user_model

class AccountTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="test@test.com", password="password", nom="Test", prenom="User")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.check_password("password"))
