from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from .views import HelloWorldView, ProductListView, ProductDetailView, ProductFilterView

# URL patterns
urlpatterns = [
    # Application endpoints
    path('', HelloWorldView.as_view(), name='hello_world'),
    path('products/', ProductListView.as_view(), name='product_list_create'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/filter/', ProductFilterView.as_view(), name='product_filter'),

    # drf-spectacular endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # Provides the OpenAPI schema
    path('api/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # ReDoc
]
