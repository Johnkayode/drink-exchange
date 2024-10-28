from django.urls import path

from api.apps.products import views


urlpatterns = [
    path("", views.ListCreateProductView.as_view(), name="list_create_product"),
    path("categories/", views.ListProductCategoryView.as_view(), name="list_product_category"),
]