from django.urls import path
from . import views


app_name = 'recipes'

urlpatterns = [
    path('show_recipes_without_product/<int:product_id>/', views.recipes_without_product , name='recipes_without_product'),
    path('cook_recipe/<int:recipe_id>/', views.cook_recipe, name='cook_recipe'),
    path('add_product_to_recipe/<int:recipe_id>/<int:product_id>/<int:weight>/', views.add_product_to_recipe, name='add_product_to_recipe'),
]
