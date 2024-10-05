from django.urls import path
from api.apps.base.views import PingView


urlpatterns = [
    path('', PingView.as_view(), name="ping"),
]
