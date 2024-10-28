from decimal import Decimal
from django.db import models
from api.apps.accounts.models import Business
from api.apps.base.models import BaseModel


class ProductCategory(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(BaseModel):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100, null=False, blank=False)
    sku_number = models.CharField(max_length=20, null=True, blank=True)
    categories = models.ManyToManyField(ProductCategory, related_name="products")
    description = models.TextField()

    base_price = models.DecimalField(
        decimal_places=2, max_digits=12, default=Decimal("0.00")
    )
    min_price = models.DecimalField(
        decimal_places=2, max_digits=12, default=Decimal("0.00")
    )
    max_price = models.DecimalField(
        decimal_places=2, max_digits=12, default=Decimal("0.00")
    )

    quantity = models.PositiveIntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

