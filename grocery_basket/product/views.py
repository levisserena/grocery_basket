from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Category, Product
from .paginators import CategoryPagination, ProductPagination
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = CategoryPagination


class ProductViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    pagination_class = ProductPagination
