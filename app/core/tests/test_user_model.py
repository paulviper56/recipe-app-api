from django.test import TestCase
from django.contrib.auth import get_user_model



class UserModelTest(TestCase):

    def test_create_user(self):
        email = 'test@example.com'
        password = 'test1234'

        User = get_user_model()
        user = User.objects.create_user(email=email, password=password)
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))
'''
    def test_create_user_successful_with_normalize_email(self):
        this test for normalizing the
        payload =[
            ['test1234@Example.com', 'test1234@example.com'],
            ['Test1234@Example.com', '']
        ]

'''