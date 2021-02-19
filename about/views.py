from django.shortcuts import render


def about_author(request):
    """"
    Выводит страницу автора.
    """
    response = render(request, 'about/author.html', )
    return response


def about_tech(request):
    """"
    Выводит страницу об использованных технологиях.
    """
    response = render(request, 'about/tech.html', )
    return response
