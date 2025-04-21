from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)  # Product name
    description = models.TextField(blank=True, null=True)  # Product description
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Product price
    stock = models.IntegerField()  # Quantity of the product in stock
    created_at = models.DateTimeField(auto_now_add=True)  # Created timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Updated timestamp

    def __str__(self):
        return self.name  # Display the name of the product in the admin panelfrom django.db import models

# Create your models here.
