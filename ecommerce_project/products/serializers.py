from rest_framework import serializers
from .models import Product ,Category



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product  # Link it to the Product model
        fields = '__all__'  # Serialize all fields


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  # Link it to the Category model
        fields = '__all__'  # Serialize all fields
