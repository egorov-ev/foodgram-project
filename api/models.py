from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

from recipes.models import Recipe

User = get_user_model()


class Favorite(models.Model):
    """
    Модель избранных рецептов.
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorites',
                             verbose_name='Пользователь', )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favored_by',
                               verbose_name='Рецепт в избранном', )

    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'recipe'],
                                        name='unique_favorite')]
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'избранные рецепты'


class Subscription(models.Model):
    """
    Модель подписки на авторов.
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Подписался на', )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Подписчик', )

    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'author'],
                                        name='unique_subscription')]
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'


class Purchase(models.Model):
    """
    Модель списка покупок пользователя.
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='purchases',
                             verbose_name='Пользователь', )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт в покупках', )

    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'recipe'],
                                        name='unique_purchase')]
        verbose_name = 'покупка'
        verbose_name_plural = 'покупки'
