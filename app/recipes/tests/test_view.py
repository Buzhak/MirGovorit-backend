from django.test import Client, TestCase
from django.urls import reverse

from recipes.models import Ingredient, Product, Recipe


BREAD = 'хлеб'
BUTTER = 'масло'
CHEES = 'сыр'
MILK = 'молоко'
SANDWICH = 'бутерброд'
HOT_MILK = 'горячее молоко'


class ViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        
        bread = Product.objects.create(title=BREAD)
        butter = Product.objects.create(title=BUTTER)
        chees = Product.objects.create(title=CHEES)
        milk = Product.objects.create(title=MILK)

        sandwich = Recipe.objects.create(title=SANDWICH)
        hot_milk = Recipe.objects.create(title=HOT_MILK)

        ingredients_to_create = [
            Ingredient(product=bread, amount=50, recipe=sandwich),
            Ingredient(product=butter, amount=20, recipe=sandwich),
            Ingredient(product=milk, amount=150, recipe=hot_milk)
        ]
        Ingredient.objects.bulk_create(ingredients_to_create)
    
    def setUp(self):
        self.guest_client = Client()

    def test_cook_recipe(self):
        """
        Проверка view cook_recipe
        """
        bread_count = Product.objects.get(title=BREAD).count
        butter_count = Product.objects.get(title=BUTTER).count
        milk_count = Product.objects.get(title=MILK).count

        self.guest_client.get(reverse(
            'recipes:cook_recipe',
            kwargs={'recipe_id': 1}
        ))

        message = 'Количество этого продукта должно изменяться на 1'

        self.assertEqual(Product.objects.get(title=BREAD).count, bread_count+1, message)
        self.assertEqual(Product.objects.get(title=BUTTER).count, butter_count+1, message)
        self.assertEqual(Product.objects.get(title=MILK).count, milk_count+1, message.replace('должно', 'не должно'))