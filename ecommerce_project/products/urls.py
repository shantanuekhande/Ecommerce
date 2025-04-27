from .views import HelloWorldView, ProductListView, ProductDetailView, ProductFilterView
from django.urls import path

urlpatterns = [
    path('', HelloWorldView.as_view(), name='hello_world'),
    path('products/', ProductListView.as_view(), name='product_list_create'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/filter/', ProductFilterView.as_view(), name='product_filter'),
]

