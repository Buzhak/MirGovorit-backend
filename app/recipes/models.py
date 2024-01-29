from django.db import models

from django.core.validators import MinValueValidator


class Product(models.Model):
    title = models.CharField('название продукта', max_length=100)
    count = models.PositiveIntegerField(
        'Количество приготовленных блюд с этим продуктом',
        default=0,
        editable=False
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self) -> str:
        return f'{self.title}'


class Recipe(models.Model):
    title = models.CharField('название рецепта', max_length=256)
    pub_date = models.DateTimeField('дата', auto_now_add=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return f'Рецепт: {self.title}'


class Ingredient(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Ингредиенты')
    amount = models.PositiveIntegerField(
        'количество', validators=[MinValueValidator(1)]
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Рецепты'
    )

    def __str__(self) -> str:
        return (
            f'{self.product.title} - '
            f'{self.amount}г'
        )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        constraints = [
            models.UniqueConstraint(
                fields=('product', 'recipe'),
                name='unique_ingredients'
            )
        ]
