from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

urlpatterns = [
    path(f"{settings.ADMIN_PREFIX}/", admin.site.urls),
    path("data/", include("data_core.urls")),
    path("", lambda request : redirect("data_core:index")),
    path('api-auth/', include('rest_framework.urls'))
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls")),]

