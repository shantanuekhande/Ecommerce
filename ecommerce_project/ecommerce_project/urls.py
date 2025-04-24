from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Configure Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="Product API Documentation",
        default_version="v1",
        description="API documentation for Product APIs.",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),  # Including URLs from the 'products' app

    # Add Swagger and Redoc endpoints
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
