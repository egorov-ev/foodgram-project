# from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

User = get_user_model()


class Ingredient(models.Model):
    """
    TBD
    """
    title = models.CharField('Название ингредиента',
                             max_length=150,
                             db_index=True
                             )
    # dimension = models.CharField('Единица измерения', max_length=10)
    unit_measure = models.CharField('Единица измерения', max_length=5)

    # quantity = models.Count('Количество', )

    class Meta:
        ordering = ('title',)
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return f'{self.title}, {self.unit_measure}'


class Recipe(models.Model):
    """
    TBD
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации (пользователь)'
    )
    title = models.CharField('Название рецепта', max_length=200)
    image = models.ImageField('Картинка',
                              upload_to='grocery_assistant/recipes/img/')
    text = models.TextField('Текстовое описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиент'
    )
    cooking_time = models.PositiveSmallIntegerField('Время приготовления')
    # slug = AutoSlugField(populate_from='title', allow_unicode=True)
    slug = models.SlugField(unique=True, verbose_name="Slug рецепта")
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Теги'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    """
    TBD
    """
    ingredient = models.ForeignKey(Ingredient,
                                   verbose_name='Ингредиент',
                                   on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='ingredients_amounts'
                               )
    quantity = models.DecimalField(max_digits=6,
                                   decimal_places=1,
                                   verbose_name='Количество',
                                   validators=[MinValueValidator(1)]
                                   )

    class Meta:
        unique_together = ('ingredient', 'recipe')
        verbose_name = 'ингредиент рецепта'
        verbose_name_plural = 'ингредиенты в рецепте'


class Tag(models.Model):
    """
    TBD
    """
    title = models.CharField('Имя тега', max_length=50, db_index=True)
    display_name = models.CharField('Имя тега для шаблона', max_length=50)
    color = models.CharField('Цвет тега', max_length=50)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.title


class Favorite(models.Model):
    """
    TODO Заполнить
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favored_by',
        verbose_name='Рецепт в избранном',
    )

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class Subscription(models.Model):
    """
    TODO Заполнить
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписался на',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписчик',
    )

    class Meta:
        unique_together = ('user', 'author')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
