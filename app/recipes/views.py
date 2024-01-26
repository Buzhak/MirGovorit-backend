from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.http import HttpResponse

from .models import Product, Recipe


TITLE_WITHOUT_PRODUCT = 'Рецепты не содержащие продукт:'


@require_GET
def recipes_without_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    recipes = Recipe.objects.prefetch_related(
        'ingredients'
    ).filter(
        ~Q(
            ingredients__product=product
        ) | Q(
            ingredients__product=product
        ) & Q(
            ingredients__amount__lt=10
        )
    ).all().order_by('id')
    template = 'recipes/recipes_without_product.html'
    context = {
        'recipes': recipes,
        'title': TITLE_WITHOUT_PRODUCT + f' {product}'
    }
    return render(request, template, context) 
