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

from django.views.decorators.csrf import csrf_exempt
from .serializers import ProductSerializer


def hello_world(request):
    return HttpResponse("Hello, World!")

def product_list(request):
    # Fetch all products from the Product model
    products = Product.objects.all()
    print(products)

    # Create a response to display product data
    response = ""
    for product in products:
        response += f"Name: {product.name}, Price: {product.price}, Stock: {product.stock}<br>"

    return HttpResponse(response)


def product_detail(request, id):
    try:
        # Fetch product by ID
        product = Product.objects.get(id=id)
        return HttpResponse(f"Product Name: {product.name}, Price: {product.price}, Stock: {product.stock}")
    except Product.DoesNotExist:
        # If no Product is found, raise a 404 error
        raise Http404("Product not found.")



from .serializers import ProductSerializer


# GET (Retrieve) and POST (Create)
@api_view(['GET'])
def product_list_create(request):
    # Handle GET requests to return all products
    if request.method == 'GET':
        products = Product.objects.all()  # Fetch all products
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)  # Return JSON response

    # # Handle POST requests to create a new product
    # elif request.method == 'POST':
    #     serializer = ProductSerializer(data=request.data)  # Deserialize JSON into Django object
    #     if serializer.is_valid():  # Validate the data
    #         serializer.save()  # Save the data to the database
    #         return Response(serializer.data, status=201)  # Return response with status 201 Created
    #     return Response(serializer.errors, status=400)  # Return validation errors


# GET single product
@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)  # Get a product by its primary key
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)  # Return 404 if not found

    serializer = ProductSerializer(product)  # Serialize the product
    return Response(serializer.data)  # Return the serialized data



@csrf_exempt
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





