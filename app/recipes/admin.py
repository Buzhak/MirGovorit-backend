from django.contrib import admin

from .models import Ingredient, Product, Recipe


class ChoiceInline(admin.TabularInline):
    model = Ingredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'pub_date', )
    list_filter = ('title', 'pub_date', )
    list_display_links = ('title', )
    inlines = [ChoiceInline]

    class Meta:
        model = Recipe


@admin.register(Product)
class IngedientAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'count')
    search_fields = ('title', )
    list_display_links = ('title', )
    list_per_page = 20

    class Meta:
        model = Ingredient
