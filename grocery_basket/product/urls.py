from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet

router_product = DefaultRouter()

router_product.register('category', CategoryViewSet, basename='category')
router_product.register('product', ProductViewSet, basename='product')

urlpatterns = [path('', include(router_product.urls))]
