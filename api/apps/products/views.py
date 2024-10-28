from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView, ListCreateAPIView
from api.apps.accounts.permissions import BusinessAdminPermission
from api.apps.products.models import Product, ProductCategory
from api.apps.products.serializers import ProductCategorySerializer, ProductSerializer


class ListProductCategoryView(ListAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]
    queryset = ProductCategory.objects.all()


class ListCreateProductView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, BusinessAdminPermission]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return []
        return Product.objects.filter(
            business=self.request.user.business
        ).order_by("-created_at")
        
