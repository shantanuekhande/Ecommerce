from django.contrib import admin
# Then register your model
from .models import Product

admin.site.register(Product)
