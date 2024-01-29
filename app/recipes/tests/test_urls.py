from django.test import Client, TestCase

from .constants import (
    BREAD,
    BUTTER,
    SANDWICH,
    URL_STATUS
)
from recipes.models import Ingredient, Product, Recipe


HTTP_405_METHOD_NOT_ALLOWED = 405


class ViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        bread = Product.objects.create(title=BREAD)
        butter = Product.objects.create(title=BUTTER)

        sandwich = Recipe.objects.create(title=SANDWICH)

        ingredients_to_create = [
            Ingredient(product=bread, amount=50, recipe=sandwich),
            Ingredient(product=butter, amount=20, recipe=sandwich),
        ]
        Ingredient.objects.bulk_create(ingredients_to_create)

    def setUp(self):
        self.guest_client = Client()
        self.url_status = URL_STATUS.copy()

    def test_no_author_edit_post(self):
        """
        Проверка доступности страниц при использовании GET метода.
        """
        message = 'Должен быть доступен только метод GET'

        for address, status_code in self.url_status.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status_code, message)
                response = self.guest_client.post(address)
                self.assertEqual(
                    response.status_code, HTTP_405_METHOD_NOT_ALLOWED, message
                )
