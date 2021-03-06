import pdfkit
from django.template.loader import get_template


def generate_purchases_pdf(template_name, context):
    """
    Генерация по шаблону PDF файла со списком покупок пользователя.
    """
    pdf_options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    html = get_template(template_name).render(context)
    return pdfkit.from_string(html, False, options=pdf_options)


def clearing_line(num):
    """
    Очищает строку от всего кроме цифр.
    """
    return ''.join([i for i in num if i.isdigit()])


def parse_ingredients(data):
    """
    Возвращает справочник: {название ингредиента ; количество}.
    """
    ingredients = {}
    for index, ingredient in data.items():
        if index.startswith('nameIngredient'):
            value = index.split('_')[1]
            ingredients[ingredient] = clearing_line(
                data[f'valueIngredient_{value}'])
    return ingredients
