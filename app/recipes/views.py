from django.db import transaction
from django.db.models import F, Q
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404, render

from .models import Ingredient, Product, Recipe


TITLE_WITHOUT_PRODUCT = 'Рецепты не содержащие продукт:'
MESSAGE_COOK_RECIPE = 'Данные обновлены'
MESSAGE_WRONG_WEIGHT_VALUE = 'Вес должен быть больше 0'
MESSAGE_WEIGHT_OK = 'г : добавлен в рецепт: '
HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400


@require_GET
def recipes_without_product(request, product_id):
    '''
    View функция выводит все рецепты, в которых,
    нет продукта, или есть,но его вес
    менее 10 грамм.

    :param product_id: id продукта
    '''

    product = get_object_or_404(Product, pk=product_id)
    recipes = Recipe.objects.prefetch_related(
        'ingredients'
    ).filter(
        ~Q(
            ingredients__product=product
        ) | Q(
            ingredients__product=product,
            ingredients__amount__lt=10
        )
    ).all().distinct().order_by('id')

    template = 'recipes/recipes_without_product.html'
    context = {
        'recipes': recipes,
        'title': TITLE_WITHOUT_PRODUCT + f' {product}'
    }
    return render(request, template, context)


@require_GET
@transaction.atomic
def cook_recipe(request, recipe_id):
    '''
    View функция обновляет количество продуктов
    использованнх в рецепте (recipe_id)

    :param recipe_id: id рецепта
    '''

    recipe = get_object_or_404(Recipe, pk=recipe_id)

    Product.objects.prefetch_related(
        'ingredients'
    ).filter(
        ingredients__recipe=recipe
    ).all().update(count=F('count') + 1)

    return HttpResponse(MESSAGE_COOK_RECIPE, status=HTTP_200_OK)


@require_GET
@transaction.atomic
def add_product_to_recipe(request, recipe_id, product_id, weight):
    '''
    View функция добавляет продукт
    с указанным весом весом
    в указанный рецепт.
    Если такой продукт в рецепте уже существует,
    данные о весе обновляются.
    :param recipe_id: id рецепта
    :param product_id: id добавляемого продукта
    :param weght: вес продукта
    :param weght priority: не может быть меньше или равен 0
    '''

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    product = get_object_or_404(Product, pk=product_id)

    if weight < 1:
        return HttpResponse(
            MESSAGE_WRONG_WEIGHT_VALUE, status=HTTP_400_BAD_REQUEST
        )

    defaults = {'product': product, 'amount': weight, 'recipe': recipe}

    Ingredient.objects.update_or_create(
        recipe=recipe, product=product, defaults=defaults
    )

    return HttpResponse(
        f'{product.title} {weight}{MESSAGE_WEIGHT_OK}{recipe.title}',
        status=HTTP_200_OK
    )
