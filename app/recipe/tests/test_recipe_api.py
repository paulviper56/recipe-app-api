from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

recipe_url = reverse('recipe:recipe-list')

def create_user(email='segun@example.com', password='pass1234'):
    """create user helper function"""
    return get_user_model().objects.create_user(email=email, password=password)

def detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])

def create_recipe(user, **params):
    '''create and return a simple recipe '''
    defaults = {
        'title': 'sample recipe title',
        'time_minute': 22,
        'price':Decimal('5.25'),
        'description': 'sample description',
        'link': 'http://examplle.com.recipe.pdf'
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)




class PublicRecipeAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_api_for_authentication(self):
        res = self.client.get(recipe_url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email= 'samuel@example.com',
            password = 'pass1234',
            name = 'Samuel'
        )

        self.client.force_authenticate(self.user)


    def test_retrieving_recipe_list(self):

        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(recipe_url)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_recipe_list_limted_to_user(self):

        other_user = create_user(email = 'etta@example.com', password='pass1234')
        create_recipe(user=other_user)
        create_recipe(user=self.user)
        res = self.client.get(recipe_url)

        recipe = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipe, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)

        res= self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

    def test_creating_recipe(self):
        '''test for creating recipes'''
        payload = {
            'title': 'Egusi Soup',
            'time_minute': 50,
            'price': Decimal('10.5')
        }

        res = self.client.post(recipe_url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])


        for k,v in payload.items():
            self.assertEqual(getattr(recipe, k), v)

        self.assertEqual(recipe.user, self.user)

    def test_perform_partial_update(self):
        """test performing partial update"""
        recipe = create_recipe(user=self.user)

        payload = {'title':'bake beans'}
        url = detail_url(recipe.id)

        res = self.client.patch(url, payload, format='json')
        recipe.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(payload['title'], recipe.title)
        self.assertEqual('sample description', recipe.description)

    def test_perform_full_update(self):
        """test to perform full update"""
        recipe = create_recipe(
            title = 'sweet chicken sauce',
            time_minute = 49,
            price = Decimal(12.50),
            link = "https://example.com/recipe.id",
            description = "sample description",
            user = self.user
        )

        payload = {
            'title':'chicken buritto',
            'time_minute':35,
            'price': Decimal('10.60'),
            'link': "https://example1.com/recipe.id",
            'description':'New sample description'
        }
        url = detail_url(recipe.id)
        res = self.client.put(url, payload, format='json')
        recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for i, k in payload.items():
            self.assertEqual(getattr(recipe, i), k)
        self.assertEqual(recipe.user, self.user)

    def test_user_return_error(self):
        """Test changing the recipe user result in an error"""
        new_user = create_user(email='user@example.com', password='pass1234')
        recipe = create_recipe(user=self.user)

        payload = {'user':new_user.id}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):

        recipe = create_recipe(user = self.user)
        url = detail_url(recipe.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_delete_another_user_recipe(self):
        user1 = create_user(email='etta@example.com', password='pass1234')
        recipe = create_recipe(user=user1)
        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id = recipe.id).exists())






