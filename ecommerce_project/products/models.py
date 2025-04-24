from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set on update

    class Meta:
        abstract = True  # This ensures it's used for inheritance only


class Product(TimestampedModel):
    name = models.CharField(max_length=100)  # Product name
    description = models.TextField(blank=True, null=True)  # Product description
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Product price
    stock = models.IntegerField()  # Quantity of the product in stock

    def __str__(self):
        return self.name  # Represents the product with its name in admin panel
