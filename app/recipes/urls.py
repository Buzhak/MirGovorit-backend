from django.urls import path
from . import views


app_name = 'recipes'

urlpatterns = [
    path('show_recipes_without_product/<int:product_id>/', views.recipes_without_product , name='recipes_without_product'),
]
