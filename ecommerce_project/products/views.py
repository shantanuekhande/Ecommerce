from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import drf_spectacular




class HelloWorldView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)


class ProductListView(APIView):
    def get(self, request, *args, **kwargs):
        # Logic for retrieving the list of products
        products = []  # Replace with actual product retrieval logic
        return Response({"products": products}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Logic for creating a new product
        product_data = request.data
        # Replace with actual product creation logic
        return Response({"product": product_data}, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    def get(self, request, product_id, *args, **kwargs):
        # Logic for retrieving a specific product by ID
        product = {"id": product_id}  # Replace with actual product retrieval logic
        return Response({"product": product}, status=status.HTTP_200_OK)

    def put(self, request, product_id, *args, **kwargs):
        # Logic for updating a specific product
        product_data = request.data
        # Replace with actual product update logic
        return Response({"product": product_data}, status=status.HTTP_200_OK)

    def delete(self, request, product_id, *args, **kwargs):
        # Logic for deleting a specific product
        # Replace with actual product deletion logic
        return Response({"message": "Product deleted."}, status=status.HTTP_204_NO_CONTENT)


class ProductFilterView(APIView):
    def get(self, request, *args, **kwargs):
        # Logic for filtering products (e.g., by query parameters)
        filters = request.query_params  # Access query parameters
        filtered_products = []  # Replace with actual filter logic
        return Response({"filters": filters, "products": filtered_products}, status=status.HTTP_200_OK)
