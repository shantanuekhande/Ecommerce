from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_world, name='hello_world'),
    # path('products/', views.product_list, name='product_list'),
    # path('products/<int:id>/', views.product_detail, name='product_detail'),
    # path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    # path('products/<int:pk>/', views.ProductRetrieveUpdateDeleteView.as_view(), name='product-detail')
    path('products/', views.product_list_create, name='product-list-create'),  # Lists and creates products
    path('product/<int:pk>/', views.product_detail, name='product-detail'),  # Get a single product
    path('deleteproduct/<int:id>/', views.delete_product, name='delete-product'),
    path('products/filter/', views.product_filter, name='product-filter')


]

