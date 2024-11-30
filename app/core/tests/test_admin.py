"""Test for the django admin"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminTest(TestCase):
    """Test for Django admin"""
    def setUp(self):  # the setup is executed first before the other tests
        """this allows us to setup some models at the begining
        of the different test to create user and client"""
        self.client = Client() # for simulating HTTP request without starting server
        self.admin_user = get_user_model().objects.create_superuser(
            email="samueltest@example.com", password="test1234")  # admin created
        self.client.force_login(self.admin_user)     # loggedin admin
        self.user = get_user_model().objects.create_user(
            email = "user1@example.com",
            password='user11234',
            name = "user test"
        )

    def test_user_list(self):
        """Test that users are listed on the page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user(self):
        """Test if the edit user page works """
        url = reverse('admin:core_user_change', args=[self.user.id])
        # user id is parse to individually change the user
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)


