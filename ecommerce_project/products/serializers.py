from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product  # Link it to the Product model
        fields = '__all__'  # Serialize all fields

