from django.contrib import admin
from django.urls import include, path

handler404 = 'grocery_assistant.views.page_not_found'  # noqa
handler500 = 'grocery_assistant.views.server_error'  # noqa

urlpatterns = [
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('api/', include('api.urls')),
    path("about/", include('about.urls')),
]
