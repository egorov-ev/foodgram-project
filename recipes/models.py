from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Ingredient(models.Model):
    """
    Модель ингредиента.
    """
    title = models.CharField('Название ингредиента', max_length=150,
                             db_index=True)
    unit_measure = models.CharField('Единица измерения', max_length=12)

    class Meta:
        ordering = ('title',)
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    """
    Модель рецепта
    """
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор публикации (пользователь)')
    title = models.CharField('Название рецепта', max_length=200)
    image = models.ImageField('Картинка',
                              upload_to='grocery_assistant/recipes/img/')
    text = models.TextField('Текстовое описание')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         verbose_name='Ингредиент')
    cooking_time = models.PositiveSmallIntegerField('Время приготовления')
    slug = AutoSlugField(populate_from='title',
                         allow_unicode=True,
                         unique=True)
    tags = models.ManyToManyField('Tag',
                                  related_name='recipes',
                                  verbose_name='Теги')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    """
    Модель хранящая в себе связь рецепта и ингредиента.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='ingredients_amounts')
    ingredient = models.ForeignKey(Ingredient, verbose_name='Ингредиент',
                                   on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [UniqueConstraint(fields=['ingredient', 'recipe'],
                                        name='unique_recipe')]
        verbose_name = 'ингредиент рецепта'
        verbose_name_plural = 'ингредиенты в рецепте'


class Tag(models.Model):
    """
    Модель "тэга".
    """
    TAG_BREAKFAST = 'breakfast'
    TAG_LUNCH = 'lunch'
    TAG_DINNER = 'dinner'
    TAG_CHOICES = [
        (TAG_BREAKFAST, 'breakfast'),
        (TAG_LUNCH, 'lunch'),
        (TAG_DINNER, 'dinner'),
    ]
    title = models.CharField('Имя тега',
                             choices=TAG_CHOICES,
                             max_length=50,
                             db_index=True)
    display_name = models.CharField('Имя тега для шаблона', max_length=50)
    color = models.CharField('Цвет тега', max_length=50)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.title


class Comment(models.Model):  # TODO: реализовать комментарии к рецепту
    """
    Модель комментария к рецепту.
    """
    post = models.ForeignKey(Recipe,
                             on_delete=models.SET_NULL,
                             related_name='comments', blank=True, null=True,
                             verbose_name='Комментарий к рецепту', )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор комментария',
                               related_name='comments', )
    text = models.TextField(max_length=1000,
                            verbose_name='Текст комментария', )
    comment_pub_date = models.DateTimeField('date published',
                                            auto_now_add=True,
                                            db_index=True)

    class Meta:
        ordering = ('comment_pub_date',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return self.post
