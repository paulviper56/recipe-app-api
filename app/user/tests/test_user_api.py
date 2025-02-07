"""Test user api """

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')
# next create a helper function that will help us to create and return a user

def create_user(**params):
    """Create and return a user """
    return get_user_model().objects.create_user(**params)

# next separate the tests into public and private test
# public being unauthenticated user i.e registering new user

class PublicUserApiTest(TestCase):

    def SetUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'email':'Test@example.com',
            'password': 'pass1234',
            'name': 'testname',
        }
        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exist_error(self):
        """Test error return if user with email exist"""

        payload = {
            'email':'Test2@example.com',
            'password':'pass1234',
            'name': 'borito',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



    def test_password_too_short(self):
        payload ={
            'email':'Test2@example.com',
            'password':'pw',
            'name': 'borito',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_users(self):
        """Test generates token for valid credentials"""
        user_details = {
            'name': 'test name borito',
            'email': 'test@example.com',
            'password': 'pass1234'
        }
        create_user(**user_details)

        payload ={
            'email': user_details['email'],
            'password': user_details['password']
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    def test_create_token_bad_credentials(self):
        """Test returns error if credentials are bad"""
        create_user(email='test@example.com', password='pass1234', name='borito')
        payload ={
            'email': 'test@example.com',
            'password': 'pass'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """test posting blank password returns an error"""
        create_user(email='test@example.com', password='pass1234')
        payload = {
            "email": "test@example.com",
            "password": ""
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def retrieve_user_unauthorized(self):
        """Test authentication is required"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateAPIUserTests(TestCase):
    """Test for authenticated users"""
    def setUp(self):
        self.user = create_user(
            email = 'test@example.com',
            password = 'pass1234',
            name = 'borito'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,{
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_not_allowed(self):
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {'name':'updated_name', 'password':'snr man'}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(self.user.name, payload['name'])
