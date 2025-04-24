from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Product
from django.http import HttpResponse, Http404
from rest_framework import generics
from .models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product



from django.views.decorators.csrf import csrf_exempt
from .serializers import ProductSerializer

@api_view(['GET'])
def hello_world(request):
    return HttpResponse("Hello, World!")
@api_view(['GET'])
def product_list(request):
    # Fetch all products from the Product model
    products = Product.objects.all()
    print(products)

    # Create a response to display product data
    response = ""
    for product in products:
        response += f"Name: {product.name}, Price: {product.price}, Stock: {product.stock}<br>"

    return HttpResponse(response)

@api_view(['GET'])
def product_detail(request, id):
    try:
        # Fetch product by ID
        product = Product.objects.get(id=id)
        return HttpResponse(f"Product Name: {product.name}, Price: {product.price}, Stock: {product.stock}")
    except Product.DoesNotExist:
        # If no Product is found, raise a 404 error
        raise Http404("Product not found.")




# Define the view function for GET and POST
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve all products.",
    responses={200: ProductSerializer(many=True)}
)
@swagger_auto_schema(
    method='post',
    operation_description="Create a new product.",
    request_body=ProductSerializer,
    responses={
        201: ProductSerializer,
        400: "Validation error. Data provided is not valid."
    }
)
@api_view(['GET', 'POST'])
def product_list_create(request):
    """
    Handle GET requests to return all products or POST requests to create a new product.
    """
    # Handle GET requests to return all products
    if request.method == 'GET':
        products = Product.objects.all()  # Fetch all products
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)  # Return JSON response

    # Handle POST requests to create a new product
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)  # Deserialize JSON into Django object
        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save the data to the database
            return Response(serializer.data, status=201)  # Return response with status 201 Created
        return Response(serializer.errors, status=400)  # Return validation errors

# GET single product
@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)  # Get a product by its primary key
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)  # Return 404 if not found

    serializer = ProductSerializer(product)  # Serialize the product
    return Response(serializer.data)  # Return the serialized data


@api_view(['DELETE'])
def delete_product(request, id):
    print(f"Received HTTP Method: {request.method}")  # Log the HTTP method
    try:
        # Attempt to find the product by ID
        product = Product.objects.get(id=id)
        product.delete()
        return Response({"message": f"Product with ID {id} deleted successfully."}, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='get',
    operation_description="Filter products by price, name, or description.",
    manual_parameters=[
        openapi.Parameter(
            'price', openapi.IN_QUERY, description="Filter by price greater than this value", type=openapi.TYPE_NUMBER
        ),
        openapi.Parameter(
            'name', openapi.IN_QUERY, description="Filter by part of the product name (case-insensitive)",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'description', openapi.IN_QUERY, description="Filter by part of the product description (case-insensitive)",
            type=openapi.TYPE_STRING
        )
    ],
    responses={200: ProductSerializer(many=True)}
)
@api_view(['GET'])
def product_filter(request):
    """
    API endpoint to filter products by price (greater than), name, or description.
    """
    # Get all products initially
    queryset = Product.objects.all()

    # Query parameters
    price = request.GET.get('price')
    name = request.GET.get('name')
    description = request.GET.get('description')

    # Apply filters as necessary
    if price:
        queryset = queryset.filter(price__gt=price)  # Filter products with price greater than the given value
    if name:
        queryset = queryset.filter(name__icontains=name)  # Filter products by name (case-insensitive, contains query)
    if description:
        queryset = queryset.filter(description__icontains=description)  # Filter products by description

    # Serialize the resulting queryset
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


#
#
# # List all products or create a new product
# class ProductListCreateView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()  # All Product objects
#     serializer_class = ProductSerializer  # Use the ProductSerializer
#
#
# # Retrieve, update, or delete a specific product
# class ProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer





