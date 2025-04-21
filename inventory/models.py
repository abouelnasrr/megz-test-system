from django.db import models
from shop.models import Products  # assuming Products is in shop app

class StockWarning(models.Model):
    product = models.OneToOneField(Products, on_delete=models.CASCADE)
    warning_limit = models.IntegerField()

    def __str__(self):
        return f"{self.product.title} - Limit: {self.warning_limit}"
