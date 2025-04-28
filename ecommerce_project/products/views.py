from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class HelloWorldView(APIView):
    """
    A simple hello world view.
    """

    @swagger_auto_schema(
        operation_summary="Hello World Endpoint",
        responses={
            200: openapi.Response(
                description="Successful Response",
                examples={"application/json": {"message": "Hello, World!"}}
            )
        }
    )
    def get(self, request):
        try:
            return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProductListView(APIView):
    """
    View to list all products or create a new product.
    """

    @swagger_auto_schema(
        operation_summary="Get List of Products",
        responses={
            200: ProductSerializer(many=True),
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        try:
            products = Product.objects.select_related('category').all()

            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="Create New Products",
        request_body=ProductSerializer(many=True),  # Indicate that the serializer expects a list
        responses={
            201: "Successfully created products.",
            400: "Bad Request - Validation Errors",
            500: "Internal Server Error",
        }
    )
    def post(self, request):
        try:
            products_data = request.data  # Expecting a list of products
            for product_data in products_data:
                category_name = product_data.get("category_name", None)
                category, created = Category.objects.get_or_create(name=category_name)
                product_data["category"] = category.id  # Replace category_name with category.id

            # Use the ProductSerializer with `many=True`
            serializer = ProductSerializer(data=products_data, many=True)
            if serializer.is_valid():
                serializer.save()  # Save all valid products in a batch
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log the exact error for debugging purposes (optional)
            print(f"An error occurred: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProductDetailView(APIView):
    """
    View to retrieve, update, or delete a single product by its ID.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve Product by ID",
        responses={
            200: ProductSerializer,
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="Update Product by ID",
        request_body=ProductSerializer,
        responses={
            200: ProductSerializer,
            400: "Bad Request",
            404: "Not Found",
            500: "Internal Server Error",
        }
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
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="Delete Product by ID",
        responses={
            200: "Product deleted successfully.",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
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
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProductFilterView(APIView):
    """
    View to filter products based on specific criteria.
    """

    @swagger_auto_schema(
        operation_summary="Filter Products",
        manual_parameters=[
            openapi.Parameter(
                "name",
                openapi.IN_QUERY,
                description="Filter by product name (partial text match)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "category",
                openapi.IN_QUERY,
                description="Filter by category ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "price",
                openapi.IN_QUERY,
                description="Filter by minimum product price",
                type=openapi.TYPE_NUMBER
            ),
        ],
        responses={
            200: ProductSerializer(many=True),
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        try:
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
