from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages.views import flatpage
from django.urls import include, path

handler404 = 'grocery_assistant.views.page_not_found'  # noqa
handler500 = 'grocery_assistant.views.server_error'  # noqa

# TODO: Добавить страницы шаблоны страниц: about_author и about_tech

flatpages_urls = [
    path('', flatpage, {'url': '/author/'}, name='about_author'),
    path('', flatpage, {'url': '/tech/'}, name='about_tech'),
]

urlpatterns = [
    path('auth/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('api/', include('api.urls')),
    path('about/', include(flatpages_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
