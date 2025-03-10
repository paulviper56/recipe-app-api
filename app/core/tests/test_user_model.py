from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models

def create_user(email='samuel56@example.com', password='pass1234'):
    return get_user_model().objects.create_user(email=email, password=password)


class UserModelTest(TestCase):

    def test_create_user(self):
        email = 'test@example.com'
        password = 'test1234'

        User = get_user_model()
        user = User.objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_successful_with_normalize_email(self):
        '''this test for normalizing the'''
        sample_email =[
            ['test1@Example.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TESt3@example.com', 'TESt3@example.com']
        ]
        for email, expected in sample_email :
            user = get_user_model().objects.create_user(
                email = email,
                password= 'pass1234'
            )
            self.assertEqual(user.email, expected)

    def test_required_email_input(self):
        ''' testing for a must required email '''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', password='pass1234')

    def test_create_superuser(self):
        email = 'test123@example.com'
        user = get_user_model().objects.create_superuser(email=email, password='pass1234')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe_model(self):
        """Test to create recipe model successfully"""
        user = get_user_model().objects.create_user(
            email= 'samuel@example.com',
            password='pass1234',
            name = 'Samuel Nnanna'
        )

        recipe = models.Recipe.objects.create(
            user = user,
            title = 'sample recipe name',
            time_minute = 5,
            price = Decimal(5.50),
            description = 'sample recipe description'
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tags_model(self):

        user = create_user()
        tag = models.Tag.objects.create(
            name= 'Dinner',
            user = user
        )

        self.assertEqual(str(tag),tag.name)