from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class HelloWorldView(APIView):
    """
    A simple hello world view.
    """

    @extend_schema(summary="Hello World Endpoint")
    def get(self, request):
        return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)


class ProductListView(APIView):
    """
    View to list all products or create a new product.
    """

    @extend_schema(summary="Get List of Products", responses=ProductSerializer(many=True))
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create a New Product",
        request=ProductSerializer,
        responses=ProductSerializer,
    )
    def post(self, request):
        try:
            category_name = request.data.get("category_name", None)
            category, created = Category.objects.get_or_create(name=category_name)
            product_data = request.data
            product_data["category"] = category.id

            serializer = ProductSerializer(data=product_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProductDetailView(APIView):
    """
    View to retrieve, update, or delete a single product by its ID.
    """

    @extend_schema(summary="Retrieve Product by ID", responses=ProductSerializer)
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        summary="Update Product by ID",
        request=ProductSerializer,
        responses=ProductSerializer,
    )
    def put(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(summary="Delete Product by ID")
    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return Response(
                {"message": "Product deleted successfully."},
                status=status.HTTP_200_OK,
            )
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )


class ProductFilterView(APIView):
    """
    View to filter products based on specific criteria.
    """

    @extend_schema(
        summary="Filter Products",
        parameters=[
            OpenApiParameter(
                "name", OpenApiParameter.QUERY, description="Name of the product", type=str
            ),
            OpenApiParameter(
                "category",
                OpenApiParameter.QUERY,
                description="Category ID of the product",
                type=int,
            ),
            OpenApiParameter(
                "price",
                OpenApiParameter.QUERY,
                description="Price of the product",
                type=float,
            ),
        ],
        responses=ProductSerializer(many=True),
    )
    def get(self, request):
        name = request.query_params.get("name")
        category = request.query_params.get("category")
        price = request.query_params.get("price")

        products = Product.objects.all()

        if name:
            products = products.filter(name__icontains=name)
        if category:
            products = products.filter(category_id=category)
        if price:
            products = products.filter(price__gte=price)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
