from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/', include("api.apps.base.urls")),
    path('api/accounts/', include("api.apps.accounts.urls")),
]
