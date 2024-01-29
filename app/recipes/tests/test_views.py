from django.db.models import Q
from django.http.response import HttpResponse
from django.test import Client, TestCase
from django.urls import reverse

from .constants import (
    CHEES,
    BREAD,
    BUTTER,
    HOT_MILK,
    MILK,
    SANDWICH,
    WEIGHT_ZERO,
    WEIGHT_LOW,
    WEIGHT_10,
    WEIGHT_HIGHT
)
from recipes.models import Ingredient, Product, Recipe


class ViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        bread = Product.objects.create(title=BREAD)
        butter = Product.objects.create(title=BUTTER)
        Product.objects.create(title=CHEES)
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
        Тестирование view cook_recipe
        """
        bread_count = Product.objects.get(title=BREAD).count
        butter_count = Product.objects.get(title=BUTTER).count
        milk_count = Product.objects.get(title=MILK).count
        path = 'recipes:cook_recipe'

        self.guest_client.get(reverse(
            path,
            kwargs={'recipe_id': 1}
        ))

        message = 'Количество этого продукта должно изменяться на +1'

        self.assertEqual(Product.objects.get(title=BREAD).count, bread_count+1, message)
        self.assertEqual(
            Product.objects.get(
                title=BUTTER
            ).count, butter_count+1, message
        )
        self.assertEqual(
            Product.objects.get(
                title=MILK
            ).count, milk_count, message.replace(
                'должно', 'не должно'
            )
        )

    def test_add_product_to_recipe(self):
        """
        Тестирование view add_product_to_recipe
        """
        chees = Product.objects.get(title=CHEES)
        sandwich = Recipe.objects.get(title=SANDWICH)

        message_data_created = 'Запись должна создаваться в БД'
        message_wrong_weight = 'Текущие данные о весе не совпадают с переданными'
        message_not_duplicate_ingredient = (
            'Запись в БД не должна дублироваться, '
            'должна изменяться текущая или добавляться новая.'
        )
        path = 'recipes:add_product_to_recipe'

        self.assertFalse(
            Ingredient.objects.filter(
                product=chees, recipe=sandwich
            ).exists()
        )

        self.guest_client.get(reverse(
            path,
            kwargs={
                'recipe_id': sandwich.id,
                'product_id': chees.id,
                'weight': WEIGHT_ZERO
            }
        ))
        self.assertFalse(
            Ingredient.objects.filter(
                product=chees, recipe=sandwich
            ).exists(), message_data_created.replace(
                'должна', 'не должна'
            )
        )

        self.guest_client.get(reverse(
            path,
            kwargs={
                'recipe_id': sandwich.id,
                'product_id': chees.id,
                'weight': WEIGHT_HIGHT}
        ))

        self.assertTrue(
            Ingredient.objects.filter(
                product=chees, recipe=sandwich
            ).exists(), message_data_created
        )
        self.assertEqual(
            Ingredient.objects.get(
                product=chees, recipe=sandwich
            ).amount, WEIGHT_HIGHT, message_wrong_weight
        )

        self.guest_client.get(reverse(
            path,
            kwargs={
                'recipe_id': sandwich.id,
                'product_id': chees.id,
                'weight': WEIGHT_LOW
            }
        ))

        self.assertEqual(Ingredient.objects.filter(
            product=chees, recipe=sandwich).count(),
            1,
            message_not_duplicate_ingredient
        )
        self.assertEqual(
            Ingredient.objects.get(product=chees, recipe=sandwich).amount,
            WEIGHT_LOW,
            message_not_duplicate_ingredient
        )

    def test_recipes_without_product(self):
        """
        Тестирование view recipes_without_product
        """
        def base_test(response: HttpResponse, product: Product, message: str) -> None:
            self.assertEqual(
                len(response.context['recipes']),
                Recipe.objects.prefetch_related(
                    'ingredients'
                ).filter(
                    ~Q(
                        ingredients__product=product
                    ) | Q(
                        ingredients__product=product,
                        ingredients__amount__lt=10
                    )
                ).all().distinct().count(),
                message
            )

        chees = Product.objects.get(title=CHEES)
        butter = Product.objects.get(title=BUTTER)
        milk = Product.objects.get(title=MILK)
        sandwict = Recipe.objects.get(title=SANDWICH)

        message = (
            'Количество записей передаваемое view',
            'функцией не соотверствует ожидаемому'
        )
        path = 'recipes:recipes_without_product'

        Ingredient.objects.filter(
            recipe=sandwict, product=chees
        ).update(amount=WEIGHT_LOW)
        response = self.guest_client.get(reverse(
            path,
            kwargs={'product_id': chees.id}
        ))
        base_test(response, chees, message)

        Ingredient.objects.filter(
            recipe=sandwict, product=chees
        ).update(amount=WEIGHT_10)
        response = self.guest_client.get(reverse(
            path,
            kwargs={'product_id': chees.id}
        ))
        base_test(response, chees, message)

        Ingredient.objects.filter(
            recipe=sandwict, product=chees
        ).update(amount=WEIGHT_HIGHT)
        response = self.guest_client.get(reverse(
            path,
            kwargs={'product_id': chees.id}
        ))
        base_test(response, chees, message)

        Ingredient.objects.create(recipe=sandwict, product=milk, amount=WEIGHT_HIGHT)
        response = self.guest_client.get(reverse(
            path,
            kwargs={'product_id': butter.id}
        ))
        base_test(response, butter, message)
